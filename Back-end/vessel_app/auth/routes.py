from flask import render_template, redirect, url_for, request, flash
from .forms import  RegistrationForm, LoginForm, UpdateAccountForm
from vessel_app.models import User
from werkzeug.utils import secure_filename
from . import bp
from PIL import Image
from io import BytesIO
from vessel_app import db, bcrypt
import pickle
from base64 import b64encode
from flask_login import login_user, current_user, logout_user, login_required
import os
import secrets


@bp.route("/login",methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('auth.account'))
            return redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)

## React to flask endpoint

@bp.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    
    form = RegistrationForm()
    if form.validate_on_submit():
        ## hashed password
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8') 
        user = User(username=form.username.data, email=form.email.data, password=hashed_password) 
        db.session.add(user)
        db.session.commit()
        print('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('auth.login'))
    else:
        print("failed to validate or create a account")
    return render_template('register.html', title='Register', form=form)

@bp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@bp.route("/account",  methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            image_data = request.files[form.picture.name].read()
            img_obj = Image.open(BytesIO(image_data))

            # save bytes image to database
            img_bytes = BytesIO()
            img_obj.save(img_bytes, format='PNG')
            img_bytes = img_bytes.getvalue()
            current_user.image_file = img_bytes

        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('auth.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

        print('getting user image')
        img_bytes = current_user.image_file

        if not img_bytes:
            print('no image')
            # no profile image
            default_image_dir = str(os.getcwd()) + r'/vessel_app/static/img/default_user.png'
            img_obj = Image.open(default_image_dir)
            img_bytes = BytesIO()
            img_obj.save(img_bytes, format='PNG')
            img_bytes = img_bytes.getvalue()
        
        
        raw_image = BytesIO(img_bytes).read()  
        profile_image = b64encode(raw_image).decode('ascii')

    return render_template('account.html', title='Account', image_file=profile_image, form=form)



