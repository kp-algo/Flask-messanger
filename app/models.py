from app import db
from flask_login import UserMixin
from datetime import datetime

class Customer(UserMixin, db.Model):
    username = db.Column(db.String(200), primary_key=True)
    password = db.Column(db.String(200), nullable=False)
    
    # Required by Flask-Login if you use a custom primary key instead of 'id'
    def get_id(self):
        return self.username

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200))
    room_id = db.Column(db.String(200)) 

class Chats(db.Model):
    chat_id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(2000))
    timestamp = db.Column(db.DateTime, default = datetime.utcnow)
    username = db.Column(db.String(200))
    room_id = db.Column(db.String(200))

class Rooms(db.Model):
    room_id = db.Column(db.String, primary_key = True)
    description = db.Column(db.String, nullable = True)
    memebers = db.Column(db.Integer)