from flask import Blueprint

bp = Blueprint('viewer_3d', __name__, template_folder='templates')

from . import routes