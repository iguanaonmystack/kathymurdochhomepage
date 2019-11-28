import os
import re
import datetime

from flask import current_app
from sqlobject import SQLObject, UnicodeCol, IntCol, StringCol, DateTimeCol
from sqlobject import SQLObjectNotFound

from .lib import helpers as h

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

