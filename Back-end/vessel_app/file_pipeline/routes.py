import os
import pydicom
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import tempfile 
import base64
import shutil
import pickle 
import logging
from datetime import datetime as dt
from PIL import Image
from io import BytesIO
from pydicom import dcmread
from pydicom.filebase import DicomBytesIO
from pydicom.charset import encode_string
from pydicom.datadict import dictionary_description as dd
from flask import render_template, url_for, flash, redirect, request, session, after_this_request, current_app, Response
from flask_login import current_user, login_required
from base64 import b64encode

## From vessel_app functions, classes, and models
from vessel_app.models import User, Dicom, DicomFormData, Object_3D
from .celery import data_pipeline
from .utils import request_id, dicom_to_thumbnail
from .vessel_pipeline_function import load_scan, get_pixels_hu, resample, sample_stack, make_lungmask, displayer, temp_file_db, pickle_vtk, unpickle_vtk, unpickle_vtk_2 
from vessel_app import db, bcrypt, dropzone

from . import bp


#### globals
path_3d = ""

@bp.before_app_request
def before_request_fun(): 
    endpoints = [rule.endpoint for rule in current_app.url_map.iter_rules()]

    if current_user.is_authenticated and request.endpoint =='file_pipeline.upload':
        # upload id
        path_3d

        session['id'] = request_id()
        print('SESSION_ID before request:', session['id'])
    if current_user.is_authenticated and request.endpoint in endpoints:
        # temp file management
        state = os.path.isdir(path_3d)

        if state:
            shutil.rmtree(path_3d)


@bp.route("/upload",  methods=['GET', 'POST'])
@login_required 
def upload():
    return render_template('upload.html')

all_files = []
file_count_global = 0

@bp.route("/dropzone_handler",  methods=['GET', 'POST'])
def dropzone_handler():

    files_list = []
    done = False

    # check if done value exists
    done = bool('done' in request.form.to_dict())

    ## request files to list of binary objects
    for key, f in request.files.items():
        if key.startswith('file'):
            files_list.append(f)

    file_count = len(files_list)
    binary_files = [file.read() for file in files_list] # list of bytes objects
    
    global all_files, file_count_global

    if not done:
        # add to overall list, but not database

        all_files.extend(binary_files)
        file_count_global += file_count
        return ''

    else:
        # add all files from post requests to database as one object

        dicom_list = []
        for byte_file in all_files: # list of all dicom files in binary
            
            # convert to dicom object
            raw = DicomBytesIO(byte_file)
            dicom_object = dcmread(raw)
            dicom_list.append(dicom_object)

        # find median dicom file to generate thumbnail
        median_i = len(dicom_list)//2
        median_dicom = dicom_list[median_i]

        ### generate thumbnail from median file
        tn_bytes = dicom_to_thumbnail(median_dicom)

        binary_blob = pickle.dumps(all_files)
        
        print("Session dropzone handler", session['id'])
        ## database upload
        batch = Dicom( 
            user_id=current_user.id,
            dicom_stack = binary_blob, 
            thumbnail = tn_bytes,
            file_count= file_count_global,
            session_id=str(session['id'])
            )

        db.session.add(batch) 
        db.session.commit()
    
        # set globals back to default values
        all_files = []
        file_count_global = 0
        return ''

@bp.route('/form', methods=['POST'])
def handle_form():

    study_name = request.form.get('study_name', "No Study Name")
    description = request.form.get('description', "No description")
    print(" SESSSION ID form_handler", session['id'])
    formData = DicomFormData( 
        study_name=study_name,
        description=description,
        session_id=str(session['id']))
    db.session.add(formData) 
    db.session.commit()

    return redirect(url_for('file_pipeline.browser'))


@bp.route('/image/<image_data>')
def get_image(image_data):
    return Response(image_data, mimetype='image/jpeg')


@bp.route('/browser')
@login_required 
def browser():
    ###### Query Database and Indexing ######
    dicom_data = Dicom.query.filter_by(user_id=current_user.id).all()
    
    #FileDataset part pydicoms
    all_studies = []
    images_list_path = []

    ######  DICOM data to dataframes function ######
    print('---- BROWSER DATA ----')
    for file_num, k in enumerate(dicom_data): #k is each row in the query database
        data = pickle.loads(k.dicom_stack)
        raw_image = BytesIO(k.thumbnail).read()
        file_count = k.file_count
        session_id = k.session_id

        print(k.formData)
        print('CARD SESSION ID:', session_id)

        study_name = k.formData.study_name
        description = k.formData.description

        ## session_id_3d
        try:
            session_id_3ds = [(k.date_uploaded, k.session_id_3d) for k in Object_3D.query.filter_by(session_id=session_id).all()]
        except:
            session_id_3ds = []

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

        # turn bytes of thumbnail into ascii string
        file_thumbnail = base64.b64encode(raw_image).decode('ascii')


        all_studies.append([study_df,
            file_thumbnail,
            file_count,
            session_id,
            session_id_3ds, 
            study_name, 
            description])

    print('------------------')

    browserFields = ["Patient's Sex", "Modality", "SOP Class UID", "X-Ray Tube Current", "FAKE FIELD"]
    #print("Print all studies list:",all_studies)
    return render_template('browser.html', all_studies=all_studies, browserFields=browserFields)

@bp.route('/job', methods=['POST'])
def job():
    if request.method == 'POST':
        session_id = request.form.get('session_id')
    else:
        return 'BAD METHOD', 500
    return render_template('job_submit.html', session_id=session_id) 

@bp.route('/delete', methods=['POST'])
def delete():
    if request.method == 'POST':
        session_id = request.form.get('session_id')
        dicom_data = Dicom.query.filter_by(session_id=session_id).first()
        data_3ds = Object_3D.query.filter_by(session_id=session_id).all()
        dicom_form_data = DicomFormData.query.filter_by(session_id=session_id).first()
        # dicom and form data
        try:
            db.session.delete(dicom_data)
            db.session.delete(dicom_form_data)
            print(dicom_data, dicom_form_data, 'deleted successfully')
        except:
            print('failed to delete', dicom_data, dicom_form_data)
            return redirect(url_for('errors.internal_error'))
        # 3d data
        if data_3ds != []:
            try:
                for data_3d in data_3ds:
                    db.session.delete(data_3d)
                    print(data_3d, 'deleted successfully')
            except:
                print('failed to delete', dicom_data, dicom_form_data)
                return redirect(url_for('errors.internal_error'))
        db.session.commit()
        print("GOING TO BROWSER")
        return redirect(url_for('file_pipeline.browser'))

    else:
        # this should never get called
        return redirect(url_for('main.index'))

@bp.route('/delete_3d', methods=['POST'])
def delete_3d():
    if request.method == 'POST':
        session_id_3d = request.form.get('session_id_3d')
        print(session_id_3d)
        object_3d_data = Object_3D.query.filter_by(session_id_3d=session_id_3d).first()
        print('attempting to delete', object_3d_data)
        try:
            db.session.delete(object_3d_data)
            db.session.commit()
            print(object_3d_data, 'deleted successfully')
            return redirect(url_for('file_pipeline.browser'))
        except:
            print('failed to delete', object_3d_data)
            flash('failed to delete', object_3d_data)
            return render_template('500.html')
    else:
        # this should never get called
        return redirect(url_for('main.index'))


@bp.route('/dicom_viewer', methods=['POST'])
def dicom_viewer():
    if request.method == 'POST':
        session_id = request.form.get('session_id')
        print('rendering dicom viewer for ID', session_id)
        dicom_data = Dicom.query.filter_by(session_id=session_id).first()
        return render_template('dicom_viewer.html') 
    else:
        # this should never get called
        return redirect(url_for('main.index'))

@bp.route('/3d_viewer', methods=['POST'])
def viewer():
    
    ## global
    global path_3d 

    print(path_3d)
    temp_dir = os.getcwd() + "\\vessel_app\\static\\users_3d_objects\\" 
    os.mkdir(path = temp_dir + "user_" + str(current_user.id))
    temp_user_dir = "user_" + str(current_user.id)
    path_3d = temp_dir + temp_user_dir

    if request.method=='POST':
        source = request.form.get('source')
        # post request came from job submit
        if source == 'job_submit':
            session_id = request.form.get('session_id')
            k = request.form.get('k')
        
            session_id_3d = str(request_id())
            k = int(request.form.get('k'))
            segmentation_options = request.form.get("segmentation_options") # blood, bone, etc.
            
            ## Calls workers
            result = data_pipeline.delay(session_id, session_id_3d, n_clusters=k)
            result_output = result.wait(timeout=None, interval=0.5)
            print(result_output)
            
            data = Object_3D.query.filter_by(session_id_3d=session_id_3d).first()
            data_a = unpickle_vtk(data.object_3D)
            path = path_3d + "\\data_object.vti"
            data_a.save(path)
            
            print(path)
            path = os.path.relpath(path, start = "vessel_app")
            path = path.replace("\\", "/")
            print("last ", path)
        #object_path = "D:\Openvessel\vessel-app\Back-end\vessel_app\static\users_3d_objects"

        # post request came from browser
        elif source == 'browser':
            session_id_3d = request.form.get('session_id_3d')
            data = Object_3D.query.filter_by(session_id_3d=session_id_3d).first()
            data_a = unpickle_vtk(data.object_3D)
            print(type(data_a))
            path = path_3d + "\\data_object.vti"
            print(path)
            data_a.save(path)
            
            print(path)
            path = os.path.relpath(path, start = "vessel_app")
            path = path.replace("\\", "/")
            print("last ", path)

        ## solution one output data as URL
            ## pathing_data = "//home//" ## sttring generate from the worker 
        
        
    return render_template('3d_viewer.html', data=data, path_data=path) 