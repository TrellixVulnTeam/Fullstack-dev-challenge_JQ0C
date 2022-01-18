import urllib
import urllib2

from bs4 import BeautifulSoup
from collections import defaultdict
import requests
from urlparse import urlparse, parse_qs
from utils import TopAppsCategory
import logging
import re

class DataScrap :
    def __init__(self):
        self.base_url = u'https://play.google.com/'
        self.regex = regex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)


    def UrlJoin(self, base_url, rel_url2):
        url1 = base_url.rstrip('/')
        url2 = rel_url2.lstrip('/')
        return url1 + '/' + url2

    def ScrapTopApps(self):
        top_apps_url = 'https://play.google.com/store/apps/top'
        data = defaultdict(lambda : {})
        page = requests.get(top_apps_url)
        soup = BeautifulSoup(page.content.decode(encoding="ascii",errors="ignore"), 'html.parser')
        result = soup.findAll('h2', string=lambda text:'top' in text.lower())
        for h2_elem in result:
            category = h2_elem.text
            # Get the url of all apps in specific category
            if(h2_elem.parent and h2_elem.parent.get('href' ,0 )):
                rel_url = self.GetHrefFromAnchor(h2_elem.parent)
                rel_url = rel_url
                if(rel_url == ''):
                    continue
                apps_page_url = self.UrlJoin(self.base_url, rel_url)
                apps = self.ScrapApps(apps_page_url)
                for app in apps.keys():
                    if data.get(app , 0):
                        data[app]['category'].append(TopAppsCategory.GetCategory(category))
                    else:
                        apps[app]['category'] = [TopAppsCategory.GetCategory(category)]
                        data[app] = apps[app]
        return data


    def ScrapApps(self , url ):
        apps = defaultdict(lambda: {})
        apps_page = requests.get(url)
        soup = BeautifulSoup(apps_page.content.decode(encoding="ascii",errors="ignore") ,'html.parser')
        #apps_url is list of anchor tags
        #anchor tags contain link to apps page
        appsDiv = soup.findAll('div',{'class': 'Vpfmgd'})


        for div in appsDiv:
            app_detail = defaultdict()
            logo = self.GetSrcFromImage(div.find('img'))
            #Name
            nameDiv = div.find('div' , class_= 'WsMG1c nnK0zc')
            name = nameDiv.text if nameDiv else ''
            #Company
            comapnyDiv = div.find('div' , class_= 'KoLSrc')
            company = comapnyDiv.text if comapnyDiv else ''
            #Ratings
            ratingParentDiv = div.find('div' , class_= 'pf5lIe')
            ratingDiv = ratingParentDiv.contents[0] if ratingParentDiv else None
            ratingText = ratingDiv.attrs['aria-label'] if ratingDiv else ''
            rating = ratingText.split()[1] if ratingText != '' else 0

            #relative url for details of app
            app_detail_rel_url = self.GetHrefFromAnchor(div.find('a' , class_= 'poRVub'))
            app_detail_url = self.UrlJoin(self.base_url, app_detail_rel_url)
            app_detail['name'] = name
            app_detail['logo'] = logo
            app_detail['company'] = company
            app_detail['rating'] = float(rating)
            app_detail['details'] = app_detail_url
            parsed_url = urlparse(app_detail_url)
            pkg_name = parse_qs(parsed_url.query)['id'][0]
            apps[pkg_name] = app_detail
        return apps

    def ScrapAppDetails(self , pkg):

        url = "https://play.google.com/store/apps/details?id=%s"%(pkg)
        details = defaultdict(lambda :'')
        page = requests.get(url)
        soup = BeautifulSoup(page.content.decode(encoding="ascii",errors="ignore"), 'html.parser')
        #resources
        resources= self.GetResources(soup)

        #genre
        genre = self.GetGenre(soup)

        #description
        description = soup.find('div',{'jsname' :'sngebd'}).text

        #image
        image = self.GetSrcFromImage(soup.find('div' , class_='xSyT2c').contents[0])

        details['resources'] = resources
        details['genre']=  genre
        details['description'] = description
        details['image'] = image
        return details

    def GetGenre(self , soup):
        companyName , genre = soup.findAll('a' , class_='hrTbp R8zArc')
        return genre.text



    def GetResources(self , soup):
        #images and videos
        resources = []

        #bttns with class Q4vdJd have child element image
        #bttns with attribute data-trailer-url contains video
        btns = soup.findAll('button', class_='Q4vdJd')

        for btn in btns :
            resources.append(self.GetSrcFromImage(btn.contents[0]))
        return resources

    def GetSrcFromImage(self, img):
        if(img.attrs.get('src',0) and re.match(self.regex ,img.attrs.get('src'))):
            return img.attrs.get('src')
        elif(img.attrs.get('data-src' , 0) and re.match(self.regex ,img.attrs.get('data-src'))):
            return img.attrs.get('data-src')
        elif(img.attrs.get('srcset' ,0) and re.match(self.regex ,img.attrs.get('srcset'))):
            return img.attrs.get('srcset')
        elif (img.attrs.get('data-src-set', 0) and re.match(self.regex ,img.attrs.get('data-src-set'))):
            return img.attrs.get('data-src-set')
        return ''

    def GetHrefFromAnchor(self , aTag):
        return aTag.attrs.get('href' , '')








