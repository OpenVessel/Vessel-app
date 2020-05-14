from vessel_app import app

from flask import render_template, url_for, flash, redirect, request, session
from flask_login import login_user, current_user, logout_user, login_required


### DO NOT forget to import app session from init file
from vessel_app import app, db, bcrypt, dropzone, photos, patch
from vessel_app.forms import RegistrationForm, LoginForm, UpdateAccountForm
from vessel_app.models import User, Upload, Upload_dicom

@app.route("/")
@app.route('/home')
def index():
    return render_template('index.html')


@app.route("/login")
def login():
       form = LoginForm()
       if form.validate_on_submit():
        
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('account'))
            
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')

    return render_template('login.html', title='Login', form=form)



