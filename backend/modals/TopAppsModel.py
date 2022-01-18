from google.appengine.ext import db

class TopAppsModel(db.Model):
    name = db.StringProperty()
    company = db.StringProperty()
    genre = db.StringProperty()
    logo = db.StringProperty()
    details = db.StringProperty()
    rating = db.FloatProperty()
    category = db.ListProperty(str)
    resources = db.ListProperty(str)
    description = db.TextProperty()
    image = db.StringProperty()



