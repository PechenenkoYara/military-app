from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Contacts(db.Model):
    number = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    occupation = db.Column(db.String(150))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    occupation = db.Column(db.String(150))
    image_file = db.Column(db.String(20), nullable=False, default='profile.png')
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    notes = db.Column(db.String(1500))
    contacts = db.relationship('Contacts')
