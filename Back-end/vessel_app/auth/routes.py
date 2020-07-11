from flask import render_template, redirect, url_for, request, flash
from .forms import  RegistrationForm, LoginForm, UpdateAccountForm
from vessel_app.models import User
from . import bp
from vessel_app import db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required
import os
import secrets


@bp.route("/login",methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('auth.account'))
            return redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)

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

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn

@bp.route("/account",  methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('auth.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file) # deprecated
    return render_template('account.html', title='Account', image_file=image_file, form=form)



