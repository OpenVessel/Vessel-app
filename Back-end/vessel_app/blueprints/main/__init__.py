from flask import Blueprint

bp = Blueprint('main', __name__, template_folder='templates')

from vessel_app.blueprints.main import routes