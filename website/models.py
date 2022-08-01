from email.policy import default
from tabnanny import check
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

class Qnas(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sector_id = db.Column(db.Integer, db.ForeignKey('sector.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    enabled = db.Column(db.Boolean, default=True)
    check = db.Column(db.Integer, default=0)
    sent = db.Column(db.Integer, default=0)

class Answers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    qnas_id = db.Column(db.Integer, db.ForeignKey('qnas.id'))
    answer = db.Column(db.String(500))

class Questions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    qnas_id = db.Column(db.Integer, db.ForeignKey('qnas.id'))
    question = db.Column(db.String(500))

class Contexts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    qnas_id = db.Column(db.Integer, db.ForeignKey('qnas.id'))
    context = db.Column(db.String(500))