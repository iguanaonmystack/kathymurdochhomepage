import os

from flask import Flask

from kathymurdochhomepage.blueprints.root import root
from kathymurdochhomepage.blueprints.recipes import recipes
from kathymurdochhomepage.lib import helpers
from kathymurdochhomepage.lib.extensions import cache, genshi
from kathymurdochhomepage.lib import model_setup

config = {
    # Flask specific configs:
    'DEBUG': True,

    # Flask-Caching related configs:
    'CACHE_TYPE': 'filesystem',
    'CACHE_DEFAULT_TIMEOUT': 300,
    'CACHE_DIR': 'flask-cache',
    'CACHE_THRESHOLD': 50,
    'CACHE_OPTIONS': {'mode': 0o600},

    # Model:
    'SQLOBJECT.DBURI': 'sqlite:knm.sqlite',
    'STORAGE.DIR': os.path.join(os.path.abspath(os.curdir), 'storage'),
}

app = Flask(__name__)
app.config.from_mapping(config)
genshi.init_app(app)
cache.init_app(app)
model_setup.setup(app.config['SQLOBJECT.DBURI'])

app.register_blueprint(root)
app.register_blueprint(recipes, url_prefix='/recipes')

@app.context_processor
def inject_helpers():
    return dict(
        h=helpers,
        tg=helpers, # backwards compatibility with old TurboGears templates
    )

