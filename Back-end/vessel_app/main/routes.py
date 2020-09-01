from flask import render_template, current_app
from vessel_app.models import User
from flask_login import login_user
from . import bp

@bp.route("/")
@bp.route('/home')
@bp.route('/index')
def index():

    if current_app.config['DEMO']:  
        ####### Login user (for demo) ###########
        print('logging in user')
        user = User.query.filter_by(email=current_app.config['DEMO_EMAIL']).first()
        login_user(user)


    return render_template('home.html')

@bp.route("/getting_started")
def getting_started():
    return render_template('getting_started.html')


