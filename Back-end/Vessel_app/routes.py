import os
import secrets
import pydicom

from PIL import Image
from pydicom import dcmread
from pydicom.filebase import DicomBytesIO
from pydicom.charset import encode_string
from flask import render_template, url_for, flash, redirect, request, session

## DO NOT forget to import app session from init
from vessel_app import app, db, bcrypt, dropzone, photos, patch
from vessel_app.forms import RegistrationForm, LoginForm, UpdateAccountForm
from vessel_app.models import User, Upload, Dicom

from flask_login import login_user, current_user, logout_user, login_required
from io import BytesIO
import pickle

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

@app.route("/register", methods=['GET', 'POST'])
def register():
    print("connect to reg page")
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RegistrationForm()
    print("form var sett")
    if form.validate_on_submit():
        print("failed")
        ## hashed password
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8') 
        user = User(username=form.username.data, email=form.email.data, password=hashed_password) 
        db.session.add(user)
        db.session.commit()
        print('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    else:
        print("failed")
        
    return render_template('register.html', title='Register', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index'))

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
    
@app.route("/account",  methods=['GET', 'POST'])
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
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    
    return render_template('account.html', title='Account', image_file=image_file, form=form)

@app.route("/documentation")
def doc():
       
    return render_template('documentation.html')
    

@app.route("/upload",  methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            print('No file part')
            return redirect(request.url)

        files = request.files.getlist("file")

        file_list = []
        for file in files:
            file_list.append(file.read())
            print("it works")
       # PIK = os.path.join(app.config['UPLOAD_FOLDER'], 'dicom_bin.dat')
      #  with open(PIK, "wb") as f:
            test = pickle.dumps(file_list)
            filename = "file name"
            ## database upload
            batch = Dicom( user_id=current_user.id, study_name=filename, dicom_stack = test ) 
            db.session.add(batch) 
            db.session.commit()
                
        return redirect(url_for('browser'))

    return render_template('upload.html')

@app.route('/results')
def results():
        # redirect to home if no images to display
   
        
    if "file_urls" not in session or session['file_urls'] == []:
        return redirect(url_for('upload'))
        
    # set the file_urls and remove the session variable
    file_urls = session['file_urls']
    session.pop('file_urls', None)
    
    return render_template('results.html', file_urls=file_urls)
    
@app.route('/browser')
def browser():

    ###### Query Database and Indexing ######
    dicom_data = Dicom.query.filter_by(user_id=current_user.id).all()
    master_list = []

    for k in dicom_data: #k is each row in the query
            data = pickle.loads(k.dicom_stack) 
            dicom_list = []
            for byte_file in data: # list of all dicom files in binary
              raw = DicomBytesIO(byte_file)
              dicom_list.append(dcmread(raw))
            master_list.append(dicom_list)

    ### Generate Thumbnail display 
    for i in master_list:
        master_list[i]



    PIK = os.path.join(app.config['UPLOAD_FOLDER'], 'dicom_bin.dat')
    with open(PIK, "rb") as f:
        data = pickle.load(f)
        return render_template('browser.html', data=data)