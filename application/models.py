from application import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True)
    password_hash = db.Column(db.String(128))
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def valid_password(self, password):
        return check_password_hash(self.password_hash, password)
    
class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    imagename = db.Column(db.String(30))
    path = db.Column(db.String(100))
    userid = db.Column(db.Integer)

class Result(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    imageid = db.Column(db.Integer)
    classid = db.Column(db.Integer)
    score = db.Column(db.Integer)
    description = db.Column(db.Text)

class Class(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    classname = db.Column(db.String(20))
    classtext = db.Column(db.Text)
    

    
