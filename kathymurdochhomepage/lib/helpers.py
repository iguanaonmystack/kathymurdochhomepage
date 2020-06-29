import os
import re
import cgi

import bleach
from flask import current_app as app
from flask import request
import werkzeug

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

def url(path=None, params=None):
    '''replacement for old turbogears.url()'''
    if path is None:
        path = request.path
    url = path
    if params:
        url += "?" + werkzeug.urls.url_encode(params)
    return url


def paramsreplace(oldparams, newparams):
    assert isinstance(oldparams, werkzeug.datastructures.MultiDict)
    if isinstance(newparams, werkzeug.datastructures.MultiDict):
        newparams = newparams.to_dict(flat=False)
    for param, values in newparams.items():
        oldparams.setlist(param, values)
    return oldparams


def paramsadd(oldparams, newparams):
    assert isinstance(oldparams, werkzeug.datastructures.MultiDict)
    oldparams.update(newparams)
    return oldparams


def params():
    return request.args


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

