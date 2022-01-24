import sys
from DataScrap import DataScrap
import modals
from utils import TopAppsCategory
import json
from collections import defaultdict
import urlparse
import logging

from google.appengine.ext import db
from google.appengine.ext import gql
from google.appengine.api import memcache
# from google.appengine.api import namespace_manager
# import requests
# import re
import cgi
# import sys
import wsgiref.handlers
# import  urllib2
# import datetime
# import os
# from google.appengine.api import users
from google.appengine.api import taskqueue
# from bs4 import BeautifulSoup
import requests_toolbelt.adapters.appengine
requests_toolbelt.adapters.appengine.monkeypatch()
# import json

import webapp2



class HelloWebapp2(webapp2.RequestHandler):
    def get(self):
        self.response.write('Hello')

class StoreAppsInDB(webapp2.RequestHandler):
    def get(self):
        task = taskqueue.add(
            url='/scraptopapps',
            target='worker',
            queue_name='TopAppsScrappper')
        try:
            memcache.flush_all()
        except BaseException as err:
            logging.error(err)
        self.response.write('Scrapped Apps')

class TopApps():
    def getApps(self, type, x = None):
        key = type + ('' if x is None else ':{0}'.format(x))
        cachedResult = memcache.get(key)
        result =[]
        if(cachedResult is None):
            topApps = modals.TopAppsModel()
            apps = topApps.gql("WHERE category = '%s'"%(type)).run(limit=x)
            for app in apps :
                result.append({'company' : app.company , 'pkg_name' : app.key().name() , 'logo' : app.logo , 'name' : app.name})

            memcache.set(key , result)
        else:
            result = cachedResult

        return result

class TopFreeApps(webapp2.RequestHandler ,TopApps):
    def get(self):
        self.response.headers.add_header('Access-Control-Allow-Origin', '*')
        self.response.headers['Content-Type'] = 'application/json'
        result = TopApps.getApps(self, TopAppsCategory.TOP_FREE_APPS)
        self.response.write(json.dumps(result))

class TopFreeGames(webapp2.RequestHandler ,TopApps):
    def get(self):
        self.response.headers.add_header('Access-Control-Allow-Origin', '*')
        self.response.headers['Content-Type'] = 'application/json'
        result = TopApps.getApps(self, TopAppsCategory.TOP_FREE_GAMES)
        self.response.write(json.dumps(result))

class TopPaidApps(webapp2.RequestHandler ,TopApps):
    def get(self):
        self.response.headers.add_header('Access-Control-Allow-Origin', '*')
        self.response.headers['Content-Type'] = 'application/json'
        result = TopApps.getApps(self, TopAppsCategory.TOP_PAID_APPS)
        self.response.write(json.dumps(result))

class TopPaidGames(webapp2.RequestHandler ,TopApps):
    def get(self):
        self.response.headers.add_header('Access-Control-Allow-Origin', '*')
        self.response.headers['Content-Type'] = 'application/json'
        result = TopApps.getApps(self, TopAppsCategory.TOP_PAID_GAMES)
        self.response.write(json.dumps(result))

class TopGrossingApps(webapp2.RequestHandler, TopApps):
    def get(self):
        self.response.headers.add_header('Access-Control-Allow-Origin', '*')
        self.response.headers['Content-Type'] = 'application/json'
        result = TopApps.getApps(self, TopAppsCategory.TOP_GROSSING_APPS)
        self.response.write(json.dumps(result))

class TopGrossingGames(webapp2.RequestHandler ,TopApps):
    def get(self):
        self.response.headers.add_header('Access-Control-Allow-Origin', '*')
        self.response.headers['Content-Type'] = 'application/json'
        result = TopApps.getApps(self, TopAppsCategory.TOP_GROSSING_GAMES)
        self.response.write(json.dumps(result))

class TopCharts(webapp2.RequestHandler ,TopApps):
    def get(self):
        self.response.headers.add_header('Access-Control-Allow-Origin', '*')
        self.response.headers['Content-Type'] = 'application/json'
        NUM = 3
        categories = TopAppsCategory.GetAllCategories()
        result = defaultdict(lambda : {})
        for category in categories :
            apps = TopApps.getApps(self , category , NUM)
            result[category] = apps

        self.response.write(json.dumps(result))

class AppDetails(webapp2.RequestHandler):
    def get(self):
        self.response.headers.add_header('Access-Control-Allow-Origin', '*')
        self.response.headers['Content-Type'] = 'application/json'

        requested_url = self.request.url
        result ={}
        #query parameters from url
        parsed = urlparse.urlparse(requested_url)
        pkg_name = urlparse.parse_qs(parsed.query)['pkg'][0]
        #check if app details in memecache
        cachedResult = memcache.get(pkg_name)
        if(cachedResult is not None):
            self.response.write(json.dumps(cachedResult))
            return

        #check if app details already present in DB
        topApps = modals.TopAppsModel()
        query_res  = topApps.get_by_key_name(pkg_name)
        if(query_res is None):
            error ={'error ' : 'No such App exist'}
            self.response.write(json.dumps(error))

        if(len(query_res.resources)==0 ):
            ds = DataScrap()
            details = ds.ScrapAppDetails(pkg_name)
            query_res.description = details['description']
            query_res.genre = details['genre']
            query_res.resources = details['resources']
            query_res.image = details['image']
            query_res.put()

        result['name'] = query_res.name
        result['company'] = query_res.company
        result['logo'] = query_res.image
        result['details_url'] = query_res.details
        result['genre'] = query_res.genre
        result['rating'] = query_res.rating
        result['resources'] = query_res.resources
        result['description'] = query_res.description

        memcache.set(pkg_name , result)
        self.response.write(json.dumps(result))




app = webapp2.WSGIApplication([
    ('/' , HelloWebapp2),
    ('/storeapps', StoreAppsInDB),
    ('/topcharts' , TopCharts),
    ('/topfreeapps', TopFreeApps),
    ('/topfreegames' , TopFreeGames),
    ('/toppaidapps', TopPaidApps),
    ('/toppaidgames', TopPaidGames),
    ('/topgrossingapps', TopGrossingApps),
    ('/topfgrossinggames', TopGrossingGames),
    ('/appdetails',AppDetails)

], debug=True)



