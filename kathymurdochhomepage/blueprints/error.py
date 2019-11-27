import logging

log = logging.getLogger(__name__)

def error(e):
    log.debug(repr(e) + str(type(e)))
    return "oh"
