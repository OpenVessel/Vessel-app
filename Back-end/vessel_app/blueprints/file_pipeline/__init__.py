from flask import Blueprint

bp = Blueprint('file_pipeline', __name__, template_folder='templates')

from vessel_app.blueprints.file_pipeline import routes