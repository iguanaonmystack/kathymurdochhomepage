from flask import Blueprint

root = Blueprint('simple_page', __name__, template_folder='templates')

@root.route('/')
def show():
    return "Hello World"

