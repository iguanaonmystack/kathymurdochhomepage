import logging
import traceback

from flask_genshi import render_response
from werkzeug.exceptions import HTTPException

log = logging.getLogger(__name__)

def error(e):
    tb = traceback.format_exc()
    code = 500
    title = "Internal server error"
    if isinstance(e, HTTPException):
        code = e.code
        title = e.description
    if code == 500:
        log.error(tb)
    return render_response('error.html', dict(
        title = title,
        status = code),
    ), code

