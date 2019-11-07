import os
import time
import logging
import datetime
import traceback
import feedparser

from flask import Blueprint, send_from_directory, current_app
from flask_genshi import render_response

log = logging.getLogger(__name__)

root = Blueprint('simple_page', __name__, template_folder='templates')

def dw_feed():
    lj_response = {}
    start_time = time.time()
    try:
        lj_response['data'] = feedparser.parse(
            'http://iguana.dreamwidth.org/data/rss').entries[:3]
    except Exception:
        log.error('Unable to fetch DW feed: %s', traceback.format_exc())
        lj_response['data'] = []
    lj_response['time'] = time.time() - start_time
    lj_response['checked'] = datetime.datetime.now()
    log.debug("lj_response time is %s", lj_response['time'])
    return lj_response


@root.route('/')
def index():
    # log.debug("Happy TurboGears Controller Responding For Duty")
    dw_response = dw_feed()
    statuses = []
    return render_response('welcome.html',
        dict(statuses=statuses, entries=dw_response['data']))


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
