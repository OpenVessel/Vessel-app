import os
import os.path
import secrets
import pydicom
import matplotlib.pyplot as plt
import pandas as pd
import tempfile 
import base64
import shutil
import pickle 
import numpy as np
### 
import logging
from vessel_app.flask_logs import LogSetup
from datetime import datetime as dt

from PIL import Image
from io import BytesIO
from PIL import Image
from pydicom import dcmread
from pydicom.filebase import DicomBytesIO
from pydicom.charset import encode_string
from pydicom.datadict import dictionary_description as dd
from flask import render_template, url_for, flash, redirect, request, session, after_this_request
from base64 import b64encode
from os import path
from io import BytesIO


## DO NOT forget to import app session from init
from vessel_app import app, db, bcrypt, dropzone, photos, patch, celery

## From Vessel_app own functions, classes, and models
from vessel_app.forms import  RegistrationForm, LoginForm, UpdateAccountForm, SessionIDForm
from vessel_app.models import User, Dicom, DicomFormData, Object_3D
from vessel_app.graph import graphing
from vessel_app.utils import request_id

from flask_login import login_user, current_user, logout_user, login_required


### Celery app functions for datapipeline
# vessel functions 
from vessel_app.vessel_pipeline_function import load_scan, get_pixels_hu, resample, sample_stack, make_lungmask, displayer, temp_file_db, pickle_vtk


# globals
session_id = None

@app.route("/")
@app.route('/home')
def index():
    return render_template('home.html')

#### celery -A vessel_app.celery worker -l info -P gevent
#### CELERY Task Queue blocks 
@celery.task()
def data_pipeline(session_id, b):
    
    # ESSENTIAL IMPORTS
    #import numpy as np
    ## vessel functions 
    #from vessel_app.vessel_pipeline_function import load_scan, get_pixels_hu, resample, sample_stack, make_lungmask

    b = b
    
    dicom_data = Dicom.query.filter_by(session_id=session_id).first()
    print("----------",dicom_data)

    data = pickle.loads(dicom_data.dicom_stack)
    dicom_list = [] 
    for byte_file in data:
        dicom_list.append(dcmread(DicomBytesIO(byte_file)))
    
    print(type(dicom_list))
    ## STEP ONE of Masking pipeline 
    patient = load_scan(dicom_list)
    print("Patient number: 1" )
    print ("Slice Thickness: %f" % patient[0].SliceThickness)
    print ("Pixel Spacing (row, col): (%f, %f) " % (patient[0].PixelSpacing[0], patient[0].PixelSpacing[1]))

    ## STEP TWO of Masking pipeline
    image_stack = get_pixels_hu(patient)
    
    ## STEP THREE RESAMPLING
    print("Shape of CT slice before resampling", image_stack.shape)
    imgs_after_resamp, spacing = resample(image_stack, patient, [1,1,1])
    print ("Shape after resampling\t", imgs_after_resamp.shape)

    masked_lung = []

    ## STEP FOUR K-MEANS MASKING
    for img in imgs_after_resamp: #loops through images and applies mask
        masked_lung.append(make_lungmask(img))
    #print(slices)
    
    mask = np.array(masked_lung)
    print(mask)
    ###
    #####
    ##### 
    
    data = displayer(mask)
    name_path = temp_file_db()

    #print(type(data))
    print(name_path)
    print(pickle_vtk(data, name_path))

    with open(name_path, 'r') as f:
        output = f.read()
        print(output.encode)

    binary_blob = bytes(7)
    string_ok = "test"
    
    insert = Object_3D( 
    object_3D = binary_blob, 
    session_id=str(session_id),
    test = str(string_ok)
    )
    
    db.session.add(insert) 
    db.session.commit()

    #displayer(mask)

    ## step one read dicom file slice load_scan() 

    return 
######
####  BEFORE & AFTER Requesting blocks 
#####

@app.before_request
def before_request_fun(): 
    webpages = ['job','account', 'upload', 'home', 'index', 'doc', 'logout', 'browser']
    if current_user.is_authenticated and request.endpoint =='upload':
        # upload id
        global session_id
        session_id = request_id()
        print('SESSION_ID:', session_id)
    if current_user.is_authenticated and request.endpoint in webpages:
        # temp file management
        temp_dir = os.getcwd() + "\\vessel_app\\static\\media\\" 
        temp_user_dir = "user_" + str(current_user.id)
        current_user_dir = temp_dir + temp_user_dir
        state = os.path.isdir(current_user_dir)

        if state == True:
            shutil.rmtree(current_user_dir)
        elif state == False:
            return 


##### logging 
@app.after_request
def after_request(response):
    """ Logging after every request. """
 #   logger = logging.getLogger("app.access")
    #logger.info(
     #   "%s [%s] %s %s %s %s %s %s %s",
    #    request.remote_addr,
    #    dt.utcnow().strftime("%d/%b/%Y:%H:%M:%S.%f")[:-3],
    #    request.method,
     #   request.path,
     #   request.scheme,
     #   response.status,
      #  response.content_length,
     #   request.referrer,
     #   request.user_agent,
   # )
    return response


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
@login_required 
def upload():
    return render_template('upload.html')


@app.route("/dropzone_handler",  methods=['GET', 'POST'])
def dropzone_handler():
    files_list = []
    for key, f in request.files.items():
        if key.startswith('file'):
            files_list.append(f)
    file_count = len(files_list)
    binary_files = [file.read() for file in files_list] # list of bytes objects
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

    tn = graphing(median_dicom)
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

    global session_id
    ## database upload
    batch = Dicom( 
    user_id=current_user.id,
    dicom_stack = binary_blob, 
    thumbnail = tn_bytes,
    file_count= file_count,
    session_id=str(session_id))
    db.session.add(batch) 
    db.session.commit()
    return ''


@app.route('/form', methods=['POST'])
def handle_form():
    study_name = request.form.get('Study Name')
    description = request.form.get('description')
    global session_id
    formData = DicomFormData( 
        study_name=study_name,
        description=description,
        session_id=str(session_id))
    db.session.add(formData) 
    db.session.commit()
    return redirect(url_for('browser'))

@app.route('/browser')
@login_required 
def browser():
    ###### Query Database and Indexing ######
    dicom_data = Dicom.query.filter_by(user_id=current_user.id).all()

    #FileDataset part pydicoms
    all_studies = []
    images_list_path = []

    temp_dir = os.getcwd() + "\\vessel_app\\static\\media\\" 
    os.mkdir(path = temp_dir + "user_" + str(current_user.id))
    temp_user_dir = "user_" + str(current_user.id)

    ######  DICOM data to dataframes function ######
    
    for file_num, k in enumerate(dicom_data): #k is each row in the query database
        data = pickle.loads(k.dicom_stack)
        raw_image = BytesIO(k.thumbnail).read()
        file_count = k.file_count
        session_id = k.session_id
        all_rows_in_study = [] # [{}, {}, {}]
        cols = [] # list of list of each column for each 
        for byte_file in data: # list of all dicom files in binary
            raw = DicomBytesIO(byte_file)
            dicom_dict = []
            
            for k,v in dcmread(raw).items():
                try:
                    pair = (dd(k),v)
                except KeyError:
                    pair = (str(k), v)
                dicom_dict.append(pair)
            dicom_dict = dict(dicom_dict)
            # dicom_dict = dict([(dd(k),v) for k,v in dcmread(raw).items()])
            all_rows_in_study.append(dicom_dict)
            cols.append(list(dicom_dict.keys())) 
        all_encompassing_cols = list(set([x for l in cols for x in l]))     # [[a, b, c], [a, d]] --flatted, set --> [a, b, c, d]
        study_df = pd.DataFrame(all_rows_in_study, columns=all_encompassing_cols)    
        
        image_64= base64.b64encode(raw_image)
        imgdata = base64.b64decode(image_64)
        file_thumbnail = f'media/'+ temp_user_dir + f'/some_image_{file_num}.png'
        root_path = os.getcwd() 
        path = root_path + r"\vessel_app/static/"
        filespec = path + file_thumbnail
        with open(filespec, 'wb') as f:
            f.write(imgdata)
        all_studies.append([study_df,file_thumbnail,file_count,session_id])
        
        browserFields = ["Patient's Sex", "Modality", "SOP Class UID", "X-Ray Tube Current", "FAKE FIELD"]

    return render_template('browser.html', all_studies=all_studies, browserFields=browserFields)

@app.route('/job', methods=['POST'])
def job():
    if request.method == 'POST':
        session_id = request.form.get('session_id')
    
    
    return render_template('job_submit.html', session_id=session_id) 

    
@app.route('/delete', methods=['POST'])
def delete():
    if request.method == 'POST':
        session_id = request.form.get('session_id')
        dicom_data = Dicom.query.filter_by(session_id=session_id).first()
        dicom_form_data = DicomFormData.query.filter_by(session_id=session_id).first()
        print('attempting to delete', dicom_data, dicom_form_data)
        try:
            db.session.delete(dicom_data)
            db.session.delete(dicom_form_data)
            db.session.commit()
            print(dicom_data, 'deleted successfully')
            return redirect(url_for('browser'))
        except:
            print('failed to delete', dicom_data, dicom_form_data)
            flash('failed to delete', dicom_data, dicom_form_data)
            return redirect(url_for('internal_error'))
    else:
        # this should never get called
        return redirect(url_for('index'))

    
@app.route('/dicom_viewer', methods=['POST'])
def dicom_viewer():
    if request.method == 'POST':
        session_id = request.form.get('session_id')
        print('rendering dicom viewer for ID', session_id)
        dicom_data = Dicom.query.filter_by(session_id=session_id).first()


        return render_template('dicom_viewer.html') 
    else:
        # this should never get called
        return redirect(url_for('index'))

@app.route('/3d_viewer', methods=['POST'])
def viewer():
    if request.method=='POST':
        session_id = request.form.get('session_id')
        k = request.form.get('k')
        segmentation_options = request.form.get("segmentation_options")
        print(session_id, k, segmentation_options)
        
        result = data_pipeline.delay(session_id, k)
        print(result.get()) 

    return render_template('3d_viewer.html') 