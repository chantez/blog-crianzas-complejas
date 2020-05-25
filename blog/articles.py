from flask_login import UserMixin
from . import db

class Article(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    year_publish = db.Column(db.String(4))
    month_publish = db.Column(db.String(2))
    title = db.Column(db.String(255))
    htmlText = db.Column(db.String(6000))
    description = db.Column(db.String(500))
    date_publish = db.Column(db.Date)
    date_created = db.Column(db.Date)
    is_published = db.Column(db.Boolean)




