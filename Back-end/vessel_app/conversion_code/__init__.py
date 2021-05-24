from flask import Blueprint

bp = Blueprint('conversion_code', __name__, template_folder='templates')

from . import routes