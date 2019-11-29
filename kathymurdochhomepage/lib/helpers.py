import os
import re
import cgi

import bleach
from flask import current_app as app

def __getattr__(attr):
    if attr == 'dev':
        return app.debug
    else:
        raise AttributeError(attr)


true_strings = ('yes', '1', 'on', 'true')

def tweet_markup(text):
    """Escape markup, parse URIs into links."""
    text = bleach.linkify(bleach.clean(text, strip=True))
    return text

def url(path):
    '''replacement for old turbogears.url()'''
    return path

def config(value, default):
    return app.config.get(value, default)

def checker(value):
    if value:
        return 'checked'
    return None

def selector(value):
    if value:
        return 'selected'
    return None

def is_dev():
    return os.environ.get('FLASK_DEBUG', '0') == '1'

