from flask import Flask
from kathymurdochhomepage.blueprints.root import root

app = Flask(__name__)
app.register_blueprint(root)
