import os
import re
import datetime

from flask import current_app
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlobject import SQLObject, SQLObjectNotFound
from sqlobject import UnicodeCol, IntCol, StringCol, DateTimeCol, BLOBCol

from .lib import helpers as h

# You can use the installed CLI sqlobject-admin tool to create these tables:

class Recipe(SQLObject):
    title = UnicodeCol(alternateID=True)
    seo = UnicodeCol(alternateID=True)
    notes = UnicodeCol()
    preptime = IntCol()
    cooktime = IntCol()
    source = UnicodeCol()
    sourceurl = StringCol()
    ingredients = UnicodeCol()
    method = UnicodeCol()
    type = StringCol()
    serves = IntCol()
    vegetarian = IntCol()
    created = DateTimeCol(default=datetime.datetime.now)
    
    @classmethod
    def by_type(cls, type, vegetarian=False):
        sel = cls.select(cls.q.type == type, orderBy=cls.q.title)
        if vegetarian:
            sel = sel.filter(cls.q.vegetarian == 1)
        return sel

    @classmethod
    def by_seo(cls, seo):
        try:
            return cls.select(cls.q.seo == seo).getOne()
        except SQLObjectNotFound:
            return None

    @classmethod
    def make_seo(cls, title):
        seo = re.sub('[^a-z]', '-', title.lower())
        while '--' in seo:
            seo = seo.replace('--', '-')
        return seo

    @property
    def image(self):
        """Return the URL of the image for this recipe"""
        return h.url('/content/recipes/' + self.seo)

    @property
    def image_disk(self):
        """Return the filesystem location of the image for this recipe"""
        return os.path.join(
            current_app.config.get('STORAGE_DIR'),
            'recipes',
            self.seo)

class User(SQLObject, UserMixin):
    username = UnicodeCol(alternateID=True)
    display_name = UnicodeCol()
    password_hash = BLOBCol(default=b'')

    @classmethod
    def by_username(cls, username):
        try:
            return cls.select(cls.q.username == username).getOne()
        except SQLObjectNotFound:
            return None

    def get_id(self):
        '''This function is used by flask_login and actually returns the
        username, an alternative ID, rather than the database ID of the user!
        '''
        return self.username

    def set_password(self, password):
        # salted hash, thank you werkzeug:
        self.password_hash = generate_password_hash(password).encode('utf-8')

    def check_password(self, password):
        return check_password_hash(self.password_hash.decode('utf-8'), password)

