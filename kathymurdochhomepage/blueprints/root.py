from flask import Blueprint
from flask_genshi import render_response

root = Blueprint('simple_page', __name__, template_folder='templates')

@root.route('/')
def show():
    title = "genshi + flask!"
    return render_response('index.html', dict(title=title))

