from datetime import datetime
from time import time
from flask import current_app
import jwt
from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from hashlib import md5



class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    notifications = db.relationship('Notification', backref='receiver', lazy='dynamic')
    notifications_enabled = db.Column(db.Boolean)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode({'reset_password': self.id, 'exp': time() + expires_in},
                          current_app.config['SECRET_KEY'],
                          algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token,
                            current_app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)


class Listing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    aesop_id = db.Column(db.Integer)
    teacher = db.Column(db.String(256))
    position = db.Column(db.String(128))
    subject = db.Column(db.String(128))
    campus = db.Column(db.String(256))    
    begin_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    multiday = db.Column(db.Boolean)
    fullday = db.Column(db.String(128))
    notes = db.Column(db.String(1024))
    date_posted = db.Column(db.DateTime)
    date_removed = db.Column(db.DateTime)
    language = db.Column(db.String(64))
    grade = db.Column(db.String(64))
    notification_sent = db.Column(db.Boolean)



class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)    
    label = db.Column(db.String(256))
    grade = db.Column(db.String(1024))
    subject = db.Column(db.String(4096))
    language = db.Column(db.String(1024))
    campus = db.Column(db.Text)

    def remove_notification():
        Notification.query.filter(Notification.id==self.id).delete()




@login.user_loader
def load_user(id):
    return User.query.get(int(id))