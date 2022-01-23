import webapp2
import modals
from google.appengine.ext import db
from DataScrap import DataScrap
import requests_toolbelt.adapters.appengine
requests_toolbelt.adapters.appengine.monkeypatch()

class scrapApps(webapp2.RequestHandler):
    def post(self):

        ds = DataScrap()
        result = ds.ScrapTopApps()

        apps = []
        for pkg_name , app_details in result.items() :
            topApps = modals.TopAppsModel(key_name=pkg_name)
            topApps.name = app_details['name']
            topApps.company = app_details['company']
            topApps.logo = app_details['logo']
            topApps.category = app_details['category']
            topApps.rating = app_details['rating']
            topApps.details = app_details['details']
            apps.append(topApps)
            # topApps.put()

        db.put(apps)


app = webapp2.WSGIApplication([
    ('/scraptopapps' , scrapApps)
], debug=True)
