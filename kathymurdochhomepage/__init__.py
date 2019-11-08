from flask import Flask
from flask_genshi import Genshi

from kathymurdochhomepage.blueprints.root import root
from kathymurdochhomepage.lib import helpers
from kathymurdochhomepage.lib.extensions import cache, genshi

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
genshi.init_app(app)
cache.init_app(app)

app.register_blueprint(root)

@app.context_processor
def inject_helpers():
    return dict(
        h=helpers,
        tg=helpers, # backwards compatibility with old TurboGears templates
    )

