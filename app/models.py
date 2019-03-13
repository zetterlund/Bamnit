from time import time
from flask import current_app, url_for
import jwt
import ast
from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from hashlib import md5
import base64
from datetime import datetime, timedelta, timezone
import os


class PaginatedAPIMixin(object):
    @staticmethod
    def to_collection_dict(query, page, per_page, endpoint, **kwargs):
        resources = query.paginate(page, per_page, False)
        data = {
            'items': [item.to_dict() for item in resources.items],
            '_meta': {
                'page': page,
                'per_page': per_page,
                'total_pages': resources.pages,
                'total_items': resources.total
            },
            '_links': {
                'self': url_for(endpoint, page=page, per_page=per_page, **kwargs),
                'next': url_for(endpoint, page=page + 1, per_page=per_page, **kwargs) if resources.has_next else None,
                'prev': url_for(endpoint, page=page - 1, per_page=per_page, **kwargs) if resources.has_prev else None
            }
        }
        return data


class User(PaginatedAPIMixin, UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    notifications = db.relationship('Notification', backref='receiver', lazy='dynamic')
    notifications_enabled = db.Column(db.Boolean)
    token = db.Column(db.String(32), index=True, unique=True)
    token_expiration = db.Column(db.DateTime)

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

    def to_dict(self, include_email=False):
        data = {
            'id': self.id,
            'username': self.username,
            'last_seen': self.last_seen.isoformat() + 'Z',
            'notification_count': len(list(self.notifications)),
            'notifications_enabled': self.notifications_enabled,
            '_links': {
                'self': url_for('api.get_user', id=self.id),
                'notifications': url_for('api.get_notifications', id=self.id),
            }
        }
        data['notifications'] = {}
        for n in self.notifications:
            n_dict = {}
            n_dict['grade'] = ast.literal_eval(getattr(n, 'grade'))
            n_dict['subject'] = ast.literal_eval(getattr(n, 'subject'))
            n_dict['campus'] = ast.literal_eval(getattr(n, 'campus'))
            n_dict['language'] = ast.literal_eval(getattr(n, 'language'))
            n_dict['timestamp'] = getattr(n, 'timestamp').replace(tzinfo=timezone.utc).isoformat()
            data['notifications'][getattr(n, 'label')] = n_dict            
        if include_email:
            data['email'] = self.email
        return data

    def from_dict(self, data, new_user=False):
        for field in ['username', 'email']:
            if field in data:
                setattr(self, field, data[field])
        if new_user and 'password' in data:
            self.set_password(data['password'])

    def get_token(self, expires_in=3600):
        now = datetime.utcnow()
        if self.token and self.token_expiration > now + timedelta(seconds=60):
            return self.token
        self.token = base64.b64encode(os.urandom(24)).decode('utf-8')
        self.token_expiration = now + timedelta(seconds=expires_in)
        db.session.add(self)
        return self.token

    def revoke_token(self):
        self.token_expiration = datetime.utcnow() - timedelta(seconds=1)

    @staticmethod
    def check_token(token):
        user = User.query.filter_by(token=token).first()
        if user is None or user.token_expiration < datetime.utcnow():
            return None
        return user


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