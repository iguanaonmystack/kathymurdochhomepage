from flask_caching import Cache
from flask_genshi import Genshi
from flask_login import LoginManager

# This is set up in __init__.py but made available here for blueprints to use.
cache = Cache()
genshi = Genshi()
login_manager = LoginManager()
