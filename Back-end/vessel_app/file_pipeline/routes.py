import os
import pydicom
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import tempfile
import base64
import json
import shutil
import pickle
import time
import logging
from datetime import datetime as dt
from PIL import Image
from io import BytesIO
from pydicom import dcmread
from pydicom.filebase import DicomBytesIO
from pydicom.charset import encode_string
from pydicom.datadict import dictionary_description as dd
from flask import render_template, url_for, flash, redirect, request, session, after_this_request, current_app, Response, jsonify, make_response
from flask_login import current_user, login_required, login_user
from base64 import b64encode
from pydicom.dataset import Dataset
import pydicom.uid

## From vessel_app functions, classes, and models
from vessel_app.models import User, Dicom, DicomFormData, Object_3D, DicomMetaData, Cidtable
from .celery_tasks import data_pipeline, query_db_insert, load_data, lung_segmentation, pyvista_call, query_db_insert, resample
from .utils import request_id, dicom_to_thumbnail
from .vessel_pipeline_function import load_scan, get_pixels_hu, resample, sample_stack, make_lungmask, displayer, temp_file_db, pickle_vtk, unpickle_vtk, unpickle_vtk_2
from vessel_app import db, bcrypt, dropzone

from . import bp

@bp.before_app_request
def before_fun():
    internal_endpoints = [rule.endpoint for rule in current_app.url_map.iter_rules()]
    #print(internal_endpoints)
    try:
        # print("Output before -------- ",session['last_endpoint'])
        pass
    except:
        session['last_endpoint'] = 'nowhere'
        # print("Output before -------- ",session['last_endpoint'])
    
    if current_user.is_authenticated and request.endpoint =='file_pipeline.upload':

        # create session_id
        session['id'] = request_id()
        print('SESSION_ID before request:', session['id'])


    if current_user.is_authenticated and session['last_endpoint'] == 'file_pipeline.viewer_3d' and request.endpoint != 'static' and request.endpoint in internal_endpoints:
        print('just left 3d viewer')
        # BUG: WONT DELETE FILES IF THE USER LEAVES THE SITE FROM 3D VIEWER
        if os.path.isdir(session['path_3d']):
            # remove user folder

            print('removing files')
            shutil.rmtree(session['path_3d'])


@bp.after_app_request
def update_last_endpoint(response):
    try:
        session['last_endpoint']
    except:
        # No last endpoint. Set to nowhere
        session['last_endpoint'] = 'nowhere'

    if request.endpoint != 'static':
        if request.endpoint != session['last_endpoint']:
            session['last_endpoint'] = 'same'
        else:
            session['last_endpoint'] = request.endpoint

    return response


@bp.route("/upload",  methods=['GET', 'POST'])
@login_required
def upload():
    if current_app.config['DEMO']:
        return redirect(url_for('main.index'))
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
    if not done:
        # add to overall list, but not database
        global all_files, file_count_global
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
            dicom_list.append(dicom_object) ## pydicom module class 'FileDataset'
	# 'FileDataSet.Pixelspacing'
        # find median dicom file to generate thumbnail
        median_i = len(dicom_list)//2
        median_dicom = dicom_list[median_i]

        ## Metadata call  ## heres validation code/new class call for metadata checks 
        study_date = median_dicom.StudyDate
        study_id = median_dicom.StudyID
        modality = median_dicom.Modality 


        ### generate thumbnail from median file
        tn_bytes = dicom_to_thumbnail(median_dicom)

        binary_blob = pickle.dumps(all_files)

        print("Session dropzone handler", session['id'])
        ## database upload

        meta_data_batch = DicomMetaData( 
            user_id = current_user.id,
            study_date = study_date,
            study_id = study_id, 
            modality = modality,
            file_count= file_count_global,
            session_id=str(session['id']),
            thumbnail = tn_bytes
        )


        batch = Dicom(
            user_id=current_user.id,
            dicom_stack = binary_blob,
            thumbnail = tn_bytes,
            file_count= file_count_global,
            session_id=str(session['id'])
            )

        db.session.add(meta_data_batch)
        db.session.add(batch)
        db.session.commit()

        # set globals back to default values
        all_files = []
        file_count_global = 0
        return 'dropzone done'

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
    time.sleep(1.5)
    return redirect(url_for('file_pipeline.browser'))

@bp.route('/browser')
@login_required
def browser():

    print('generating browser')
    ###### Query Database and Indexing ######
    # dicom_data = Dicom.query.filter_by(user_id=current_user.id).all()
    dicom_meta_data = DicomMetaData.query.filter_by(user_id=current_user.id).all()
    cidPass = Cidtable.query.filter_by(cold_storage_id=current_user.id).all()
    print(len(dicom_meta_data))
    # form_data = DicomFormData.query.filter_by(session_id=session_id).all()
    #FileDataset part pydicoms
    all_studies = []
    images_list_path = []

    ######  DICOM data to dataframes function ######
    print('---- BROWSER DATA ----')
    for file_num, k in enumerate(dicom_meta_data): #k is each row in the query database
        raw_image = BytesIO(k.thumbnail).read()
        file_count = k.file_count
        session_id = k.session_id
        study_id = k.study_id
        study_date = k.study_date
        modality = k.modality
        form_data = DicomFormData.query.filter_by(session_id=session_id).all()
        for file_num, j in enumerate(form_data):
            study_name = j.study_name
            description = j.description       
        ## session_id_3d
        try:
            session_id_3ds = [(k.date_uploaded, k.session_id_3d) for k in Object_3D.query.filter_by(session_id=session_id).all()]
            cids =  [(k.cid) for k in Cidtable.query.filter_by(session_id=session_id).all()]

        except:
            session_id_3ds = []
            cids = []

        all_rows_in_study = [] # [{}, {}, {}]
        cols = [] # list of list of each column for each

        dicom_dict = {
        "Study Date":study_date, 
        "Study ID":study_id, 
        "Modality":modality
        }

        all_rows_in_study.append(dicom_dict)
        cols.append(list(dicom_dict.keys()))

        all_encompassing_cols = list(set([x for l in cols for x in l]))     # [[a, b, c], [a, d]] --flatted, set --> [a, b, c, d]
        study_df = pd.DataFrame(all_rows_in_study, columns=all_encompassing_cols)
        # turn bytes of thumbnail into ascii string
        file_thumbnail = base64.b64encode(raw_image).decode('ascii')

## we want to keep this study 
        all_studies.append({
            'study_df': study_df,
            'file_thumbnail': file_thumbnail,
            'file_count': file_count,
            'session_id': session_id,
            'session_id_3ds': session_id_3ds,
            'cids':cids,
            'study_name': study_name,
            'description': description
            })

    browserFields = ["Study Date", "Study ID", "Modality"]

    restoreable_cids  = []
    for cid in cidPass:
        cidNumber = cid.cid
        CidSession_id = cid.session_id

        try:
            cids =  [(k.cid) for k in Cidtable.query.filter_by(session_id=CidSession_id).all()]
        except:
            cids = []
        print(cidNumber)

        restoreable_cids.append({
            'cids':cids,
            'session_id':CidSession_id
        })

    return render_template('browser.html',
    all_studies=all_studies, ## all_studies dict?
    browserFields=browserFields,
    restoreable_cids=restoreable_cids) ## browserFields 

@bp.route('/delete', methods=['POST'])
def delete():
    if request.method == 'POST':
        session_id = request.form.get('session_id')
        dicom_data = Dicom.query.filter_by(session_id=session_id).first()
        data_3ds = Object_3D.query.filter_by(session_id=session_id).all()
        dicom_form_data = DicomFormData.query.filter_by(session_id=session_id).first()
        dicom_meta_data = DicomMetaData.query.filter_by(session_id=session_id).first()
        # dicom and form data
        try:
            db.session.delete(dicom_data)
            db.session.delete(dicom_form_data)
            db.session.delete(dicom_meta_data)
            print(dicom_data, dicom_form_data, 'deleted successfully')
        except:
            print('failed to delete', dicom_data, dicom_form_data,dicom_meta_data )
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


@bp.route('/google_drive', methods=['POST', 'GET'])
def google_drive(): 
    return 

# Web Access to DICOM Objects (WADO) this needs some desgins 
def bulk_data_handler(data_element):
    uri = store_data_and_return_uri(data_element)
    return uri

@bp.route('/fileCoinCall', methods=['POST', 'GET'])
def fileCoinCall(): 
    data_pass = None
    dataGet = request.get_json(force=True)
    print(dir(dataGet))
    print(dataGet['session_id'])
    
    cidTableCheck = Cidtable.query.filter_by(cold_storage_id=current_user.id).all()
    if(cidTableCheck != []):
        if(cidTableCheck != None):
            for cidTable in cidTableCheck:
                checkSession_id = cidTable.session_id
                if(checkSession_id == dataGet['session_id']):
                ## if session_id of the data is already uploaded we dont insert new CID 
                    print("data already stored on fileCoin")
                    messages = 'data already stored on fileCoin'
                    errors = 503
                    return jsonify(status="failure", messages=messages, errors=errors)


    if request.method == 'POST':
        print("hello query for FileCoinCall")
        session_id = dataGet['session_id'] # we removed the form so we are not passing session id 
        dicom_data = Dicom.query.filter_by(session_id=session_id).first()
        dicom_form_data = DicomFormData.query.filter_by(session_id=session_id).first()
        dicom_meta_data = DicomMetaData.query.filter_by(session_id=session_id).first()
        data = pickle.loads(dicom_data.dicom_stack)
        dicom_list = [] 
        for byte_file in data:
            dicom_list.append(dcmread(DicomBytesIO(byte_file)))
        # https://pydicom.github.io/pydicom/stable/tutorials/dicom_json.html
        list_of_json_dicom = []
        for dicom_file in dicom_list:
            
            # Web Access to DICOM Objects (WADO) 
            # list_of_json_dicom.append(dicom_file.to_json(bulk_data_element_handler=bulk_data_handler))
            # implement URI later or the  https://www.dicomstandard.org/dicomweb/retrieve-wado-rs-and-wado-uri/
            
            list_of_json_dicom.append(dicom_file.to_json())
        print(type(list_of_json_dicom))
        
        ## Call encrpytion here
        errors = 'no errors'
        ## web3.storage call first 
        try:
        # return redirect(url_for('file_pipeline.browser', data=data_pass))
            return jsonify(status="success", session_id=session_id, data=list_of_json_dicom, errors=errors)
            
        except:
            print('failed to transfer data to javascript', type(data_pass))
            flash('failed to upload data to FileCoin')
            return render_template('500.html')
    ## so we need to query data via user session idea
    # return redirect(url_for('file_pipeline.browser', data=data_pass))

    # return render_template('browser.html',
    #         data=data_pass ## all_studies dict?
    #         ) ## browserFields 


@bp.route('/storeCID', methods=['POST', 'GET'])
def storeCID(): 
    data_pass = None
    dataGet = request.get_json(force=True)
    print(dataGet)
    print("test store CID endpoint", dataGet['cid'])


    cidTableCheck = Cidtable.query.filter_by(cold_storage_id=current_user.id).all()
    if(cidTableCheck != []):
        if(cidTableCheck != None):
            for cidTable in cidTableCheck:
                checkSession_id = cidTable.session_id
                if(checkSession_id == dataGet['session_id']):
                ## if session_id of the data is already uploaded we dont insert new CID 
                    print("cid already exist is record on OpenVessel DB")
                    messages = 'cid already exist is record on OpenVessel DB'
                    errors = 503
                    return jsonify(status="failure", messages=messages, errors=errors)
                    # redirect(url_for('file_pipeline.browser'))


    ## we need some safety code to check if session ID already uploaded?
    if request.method == 'POST':
        print("store call for CID")
        cid = dataGet['cid'] # we removed the form so we are not passing session id 
        print(cid)
        print(type(cid))
        session_id = dataGet['session_id']
        #so we recevied the CID we need to store it in the database tabel
        cidTableCall = Cidtable( 
            session_id = str(session_id),
            cid = str(cid),
            cold_storage_id = current_user.id, ## retsoriation mechican for returning deleting data
        )
        db.session.add(cidTableCall)
        db.session.commit()
        
        errors = 'no errors'
        ## web3.storage call first 
        try:
            # we successelly saved CID
            # we need to redirect to browser somehow
            return jsonify(status="success", errors=errors)
            
        except:
            print('failed to save CID')
            flash('failed to save CID')
            return render_template('500.html')

@bp.route('/restoreDataObjectCID', methods=['POST', 'GET'])
def restoreDataObjectCID(): 
    
    dataGet = request.get_json(force=True)
    
    # Cidtable.query.filter_by(cid=dataGet['cid'])
    
    #Check if data is already in existence for the user
    cidTableCheck = Cidtable.query.filter_by(cid=dataGet['cid']).all()
    if(cidTableCheck != []):
        if(cidTableCheck != None):
            for cidTable in cidTableCheck:
                checkSession_id = cidTable.session_id
                if(checkSession_id):
                    DicomCheck = Dicom.query.filter_by(session_id=checkSession_id).all()
                    for dicom_row in DicomCheck:
                        DataSessionID = dicom_row.session_id
                    try: 
                        print("its does exit!",DataSessionID)
                        return jsonify(message="SessionID is exist in database already")
                    except NameError: 
                        DataSessionID = None
                        print("it does not exsit")

    if request.method == 'POST':
        test3 = json.loads(dataGet["data"])
        # print(test3["data"]) #    print(test2['session_id'])
                # TypeError: string indices must be integers
        print(type(test3["data"]))
        print(len(test3["data"]))

        dicom_list = [] 
        for test in test3["data"]:
            y = json.loads(test)
            ds1 = pydicom.dataset.Dataset.from_json(y)
            
            ds1.ensure_file_meta()
            ds1.fix_meta_info(enforce_standard=True)
            print(ds1.file_meta)
            ds1.file_meta.TransferSyntaxUID = pydicom.uid.ImplicitVRLittleEndian

            # Works!!
            # <class 'pydicom.dataset.Dataset'>
            dicom_list.append(ds1)

        median_i = len(dicom_list)//2
        median_dicom = dicom_list[median_i]

        ## Metadata call  ## heres validation code/new class call for metadata checks 
        study_date = median_dicom.StudyDate
        study_id = median_dicom.StudyID
        modality = median_dicom.Modality 

        ### generate thumbnail from median file
        tn_bytes = dicom_to_thumbnail(median_dicom)
        binary_blob = pickle.dumps(all_files)

        OldSession_ID = cidTable.session_id
        ## database upload
        file_count_restore = len(dicom_list)
        meta_data_batch = DicomMetaData( 
            user_id = current_user.id,
            study_date = study_date,
            study_id = study_id, 
            modality = modality,
            file_count= file_count_restore,
            session_id=str(OldSession_ID),
            thumbnail = tn_bytes
        )

        study_name = "Restored Study Name"
        description = "Resttored description"
        
        formData = DicomFormData(
            study_name=study_name,
            description=description,
            session_id=str(OldSession_ID)
        )

        batch = Dicom(
            user_id=current_user.id,
            dicom_stack = binary_blob,
            thumbnail = tn_bytes,
            file_count= file_count_global,
            session_id=str(OldSession_ID)
            )

        db.session.add(meta_data_batch)
        db.session.add(formData)
        db.session.add(batch)
        db.session.commit()

        print("hello restore Data")
    return jsonify(status="success")