from flask import Blueprint

bp = Blueprint('errors', __name__, template_folder='templates')

from vessel_app.blueprints.errors import errors