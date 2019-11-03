from flask import Flask
from flask_genshi import Genshi

from kathymurdochhomepage.blueprints.root import root

app = Flask(__name__)
genshi = Genshi(app)

app.register_blueprint(root)
