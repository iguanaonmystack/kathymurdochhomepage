import logging

from flask_genshi import render_response
from werkzeug.exceptions import HTTPException

log = logging.getLogger(__name__)

def error(e):
    code = 500
    title = "Internal server error"
    if isinstance(e, HTTPException):
        code = e.code
        title = e.description
    return render_response('error.html', dict(
        title = title,
        status = e.code),
    ), code

