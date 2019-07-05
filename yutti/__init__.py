from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_session_plus import Session
import redis
from config import DATABASE_URI
from werkzeug.debug import DebuggedApplication
from db_orm import db_orm
csrf = CSRFProtect()
sess = Session()

class Yutti(Flask):

    def __init__(self, import_name, config, *args, **kwargs):
        super().__init__(import_name, *args, **kwargs)
        self.config.from_mapping(
            DEBUG=True,
            SERVER_NAME='ut61a.space',
            # SESSION_TYPE = 'redis',    || Flask-session garbage
            SESSION_CONFIG = [
                # First session will store the csrf_token only on it's own cookie.
                {
                    'cookie_name': 'csrf',
                    'session_type': 'secure_cookie',
                    'session_fields': ['csrf_token'],
                },
                # Second session will store the user logged in inside the firestore sessions collection.
                {
                    'cookie_name': 'session',
                    'session_type': 'redis',
                    'session_fields': ['user_id', 'user_data'],
                    'client': redis.Redis(host='localhost', port=6272),
                    'collection': 'sessions',
                },
                # Third session will store any other values set on the Flask session on it's own secure cookie
                {
                    'cookie_name': 'data',
                    'session_type': 'secure_cookie',
                    'session_fields': 'auto'
                },
            ],


            # SESSION_REDIS = redis.Redis(host='localhost', port=6272), || Flask-session garbage
            SECRET_KEY='SO FUCKUNG STUPID',
            SQLALCHEMY_DATABASE_URI=config.DATABASE_URI
        )
        if self.debug:
            self.wsgi_app = DebuggedApplication(self.wsgi_app, evalex=True)
        self.init_csrf()
        self.init_session()
    
    def init_db(self):
        db_orm.init_app(self)

    def init_csrf(self):
        csrf.init_app(self)
    
    def init_session(self):
        sess.init_app(self)