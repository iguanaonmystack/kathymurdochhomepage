import os
import time
import logging
import datetime
import traceback
import feedparser

import magic
from flask import Blueprint, send_from_directory, current_app, abort, redirect
from flask_genshi import render_response

from ..lib.extensions import cache

log = logging.getLogger(__name__)

root = Blueprint('root', __name__, template_folder='templates')

@cache.memoize()
def homepage_feed(url):
    lj_response = {}
    start_time = time.time()
    try:
        lj_response['data'] = feedparser.parse(url).entries
    except Exception:
        log.error('Unable to fetch feed %s: %s', url, traceback.format_exc())
        lj_response['data'] = []
    lj_response['time'] = time.time() - start_time
    lj_response['checked'] = datetime.datetime.now()
    log.debug("time to fetch feed %s: %s", url, lj_response['time'])
    return lj_response


@root.route('/')
def index():
    # log.debug("Happy TurboGears Controller Responding For Duty")
    dw_response = homepage_feed(
        'https://iguana.dreamwidth.org/data/rss')['data'][:3]
    pleroma_response = homepage_feed(
        'https://social.nevira.net/users/iguana/feed.atom')['data'][:10]
    return render_response('welcome.html',
        dict(statuses=pleroma_response, entries=dw_response))


@root.route('/favicon.ico')
def favicon():
    return send_from_directory(
        os.path.join(current_app.root_path, 'static', 'images'),
        'favicon.ico', mimetype='image/vnd.microsoft.icon')

@root.route('/robots.txt')
def robots():
    return send_from_directory(
        os.path.join(current_app.root_path, 'static'),
        'robots.txt', mimetype='text/plain')

@root.route('/content/<path:path>')
def content(path):
    if '..' in path:
        logging.info('Ignoring path with ..: %s', path)
        abort(404)
    localpath = os.path.normpath(path)
    if localpath.startswith('..'):
        logging.info('Ignoring normalised path with ..: %s', localpath)
        abort(404)
    localpath = os.path.join(current_app.config['STORAGE.DIR'], localpath)
    if not os.path.isfile(localpath):
        logging.info('Local file does not exist: %s', localpath)
        abort(404)
    mime = magic.Magic(mime=True)
    mimetype = mime.from_file(localpath)
    return send_from_directory(
        current_app.config['STORAGE.DIR'], path, mimetype=mimetype)

@root.route('/about')
def about():
    age = (datetime.date.today() - datetime.date(1984, 12, 28)).days / 365.24
    # (CLOSE ENOUGH SHUT UP)
    return render_response('about.html', dict(age=int(age)))

@root.route('/l')
def l():
    return redirect('/L')

@root.route('/L')
def L():
    return render_response('L.html', dict())

@root.route('/contact')
def contact():
    return redirect('/about')

