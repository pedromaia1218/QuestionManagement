from . import db
from flask_login import UserMixin

class Sector(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150))
    iniciais = db.Column(db.String(150))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    sector_id = db.Column(db.Integer, db.ForeignKey('sector.id'))
    email = db.Column(db.String(150), unique=True)
    senha = db.Column(db.String(150))
    nome = db.Column(db.String(150))
    userType = db.Column(db.String(10))