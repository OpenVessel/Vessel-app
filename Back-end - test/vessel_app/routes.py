from vessel_app import app

from flask import render_template, url_for, flash, redirect, request, session
from flask_login import login_user, current_user, logout_user, login_required


### DO NOT forget to import app session from init file
from vessel_app import app, db, bcrypt, dropzone
#photos, patch
from vessel_app.forms import RegistrationForm, LoginForm, UpdateAccountForm
from vessel_app.models import User, Upload 
#Upload_dicom

@app.route("/")
@app.route('/home')
def index():
    return render_template('home.html')


@app.route("/login",methods=['POST', 'GET'])
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

@app.route('/browser')
def browser():

   return render_template('browser.html')

@app.route('/upload')
def upload():
    return render_template('upload.html')

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    
    form = RegistrationForm()
    if form.validate_on_submit():
      

        ## hashed password
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8') 
        user = User(username=form.username.data, email=form.email.data, password=hashed_password) 
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        
     
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)