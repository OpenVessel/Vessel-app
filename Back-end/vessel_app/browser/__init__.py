from flask import Blueprint

bp = Blueprint('browser', __name__, template_folder='templates')

from . import routes