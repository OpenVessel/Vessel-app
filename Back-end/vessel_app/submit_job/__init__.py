from flask import Blueprint

bp = Blueprint('submit_job', __name__, template_folder='templates')

from . import routes