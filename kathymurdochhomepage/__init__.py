from flask import Flask, url_for
from flask_genshi import Genshi
from flask_caching import Cache

from kathymurdochhomepage.blueprints.root import root
from kathymurdochhomepage.lib import helpers

config = {
    # Flask specific configs:
    'DEBUG': True,

    # Flask-Caching related configs:
    'CACHE_TYPE': 'filesystem',
    'CACHE_DEFAULT_TIMEOUT': 300,
    'CACHE_DIR': 'flask-cache',
    'CACHE_THRESHOLD': 50,
    'CACHE_OPTIONS': {'mode': 0o600},
}

app = Flask(__name__)
app.config.from_mapping(config)
genshi = Genshi(app)
cache = Cache(app)

app.register_blueprint(root)

@app.context_processor
def inject_helpers():
    return dict(
        h=helpers,
        tg=helpers, # backwards compatibility with old TurboGears templates
    )

