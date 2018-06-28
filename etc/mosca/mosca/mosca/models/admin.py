#-*- coding: utf-8 -*-

from mosca import db

from werkzeug import generate_password_hash, check_password_hash


class User(db.Document):
    meta = {
        'collection': 'user',
        'allow_inheritance': True,
        'indexes': ['email', 'username'],
        'ordering': ['email', 'username']
    }

    username = db.StringField(max_Length=100, unique=True)
    firstname = db.StringField(max_Length=100)
    lastname = db.StringField(max_Length=100)
    email = db.StringField(max_Length=120, unique=True)
    pwdhash = db.StringField(max_Length=54)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email.lower()
        self.set_password(password)

    @property
    def login(self):
        return self.username

    @login.setter
    def login(self, value):
        self.username = value

    def set_password(self, password):
        self.pwdhash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pwdhash, password)

    # Flask-Login integration
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.uid

    # Required for administrative interface
    def __unicode__(self):
        return self.username
