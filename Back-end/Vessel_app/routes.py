import os
import secrets
import pydicom
import matplotlib.pyplot as plt
import pandas as pd
from PIL import Image
from io import BytesIO
from PIL import Image
from pydicom import dcmread
from pydicom.filebase import DicomBytesIO
from pydicom.charset import encode_string
from pydicom.datadict import dictionary_description as dd
from flask import render_template, url_for, flash, redirect, request, session

## DO NOT forget to import app session from init
from vessel_app import app, db, bcrypt, dropzone, photos, patch
from vessel_app.forms import RegistrationForm, LoginForm, UpdateAccountForm
from vessel_app.models import User, Upload, Dicom
from vessel_app.graph import graphing

from flask_login import login_user, current_user, logout_user, login_required
from io import BytesIO
import pickle

@app.route("/")
@app.route('/home')
def index():
    return render_template('home.html')

@app.route("/login",methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('account'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/register", methods=['GET', 'POST'])
def register():

    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RegistrationForm()

    if form.validate_on_submit():
        
        ## hashed password
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8') 
        user = User(username=form.username.data, email=form.email.data, password=hashed_password) 
        db.session.add(user)
        db.session.commit()
        print('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    else:
        print("failed to validate or create a account")
        
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

        files = request.files.getlist("file") # list of FileStorage objects
        file_count = len(files)
        binary_files = [file.read() for file in files] # list of bytes objects
        binary_blob = pickle.dumps(binary_files) # binary blob

        ### generate thumbnail
        data = pickle.loads(binary_blob) 
        dicom_list = []
        for byte_file in data: # list of all dicom files in binary
            raw = DicomBytesIO(byte_file)
            dicom_list.append(dcmread(raw))

        # find median dicom file to generate thumbnail
        median_i = len(dicom_list)//2
        median_dicom = dicom_list[median_i]

        tn = graphing([median_dicom])
        
        size = (300, 300)
        tn.thumbnail(size)

        # convert thumbnail to bytes

        def imgToBytes(img):
            img_bytes = BytesIO()
            img.save(img_bytes, format='PNG')
            img_bytes = img_bytes.getvalue()

            return img_bytes
        
        tn_bytes = imgToBytes(tn)

        filename = "file name"

        ## database upload
        batch = Dicom( user_id=current_user.id,
        study_name=filename, 
        dicom_stack = binary_blob, 
        thumbnail = tn_bytes,
        file_count= file_count )
        db.session.add(batch) 
        db.session.commit()

        return redirect(url_for('browser'))

    return render_template('upload.html')

@app.route('/browser')
def browser():

    ###### Query Database and Indexing ######
    dicom_data = Dicom.query.filter_by(user_id=current_user.id).all()

#FileDataset part pydicom
    all_studies = []

######  DICOM data to dataframes function ######

    for k in dicom_data: #k is each row in the query
        data = pickle.loads(k.dicom_stack)

        # image = pickle.loads(k.thumbnail)
        image = Image.open(BytesIO((k.thumbnail)))
        print(type(image))
        all_rows_in_study = [] # [{}, {}, {}]
        cols = [] # list of list of each column for each 
        for byte_file in data: # list of all dicom files in binary
            raw = DicomBytesIO(byte_file)
            dicom_dict = dict([(dd(k),v) for k,v in dcmread(raw).items()])
            all_rows_in_study.append(dicom_dict)
            cols.append(list(dicom_dict.keys()))
            # encompassing generates set 
        all_encompassing_cols = list(set([x for l in cols for x in l]))     # [[a, b, c], [a, d]] --flatted, set --> [a, b, c, d]
        study_df = pd.DataFrame(all_rows_in_study, columns=all_encompassing_cols)    
        all_studies.append(study_df)

    
    #print(all_studies[0].columns )
    #image[0].show()
    #####3

    #print 
    #   {{ study["Patient's Sex"].iloc[0].value.decode("utf-8") }}
    ## drop down option 

    return render_template('browser.html', data=all_studies, images = image)

@app.route('/job')
def job():
    return render_template('job_submit.html')