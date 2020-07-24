from flask import render_template
from . import bp

@bp.route("/")
@bp.route('/home')
@bp.route('/index')
def index():
    return render_template('home.html')

@bp.route("/documentation")
def doc():
    return render_template('documentation.html')

