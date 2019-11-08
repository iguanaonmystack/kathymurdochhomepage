from flask_caching import Cache
from flask_genshi import Genshi

# This is set up in __init__.py but made available here for blueprints to use.
cache = Cache()
genshi = Genshi()
