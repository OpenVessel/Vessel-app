from flask import render_template, current_app, redirect, url_for, request, session
from vessel_app.models import User, FalseForm,FalseDicom
from flask_login import login_user, current_user
from . import bp
import os
import time
import pickle
from vessel_app import db, bcrypt, dropzone

from .utils import request_id, temp_session_id

from pydicom import dcmread
from pydicom.filebase import DicomBytesIO

## Global file check
all_files = []
file_count_global = 0

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


@bp.route("/conversion",  methods=['GET', 'POST'])
def conversion_page():

    session = temp_session_id(current_app, current_user)
    print('TEMP_SESSION_ID before request:', session['id'])

    if current_app.config['DEMO']:
        return redirect(url_for('conversion_page.html'))

    ## we load the webpage and check for post request 
    ## uploads data to database and 
    # converts it to the derise type and returns a zip file
    return render_template("conversion_page.html"), session

@bp.route('/convert_form', methods=['POST'])
def handle_form():
    
    ## we are going to create a false form 
    study_name = "anonymous"
    description = "no textd"
    session = temp_session

    print(" TEMP SESSSION ID form_handler", session)
    formData = FalseForm(
        study_name=study_name,
        description=description,
        session_id=str(session))
    db.session.add(formData)
    db.session.commit()

    ## instead of time deplay we need function to check if the upload is complete!!
    time.sleep(1.5)
    return ""

@bp.route("/convert_dropzone_handler",  methods=['GET', 'POST'])
def convert_dropzone_handler():
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
            dicom_list.append(dicom_object) ##
        
        
        binary_blob = pickle.dumps(all_files)

        batch = FalseDicom(
            temp_user_id=session.id,
            dicom_stack = binary_blob,
            file_count= file_count_global,
            session_id=str(session['id'])
            )

        db.session.add(batch)
        db.session.commit()

    # set globals back to default values
        all_files = []
        file_count_global = 0
        return 'dropzone done'


@bp.route('/convert', methods=['POST'])
def convert():

    if request.method == 'POST':
        file_type = request.form.get('file_types')
        session_id = request.form.get('session_id')

        if file_type == 'matlab':
            output_path = os.getcwd() + "\\vessel_app\data_saved\\matlab_session_id_{}".format(session_id)
            if os.path.exists(output_path):
                shutil.rmtree(output_path)
            dicom_data = Dicom.query.filter_by(session_id=session_id).first()
            dicom_list = query_to_dicom_list(dicom_data)
            
            print(type(dicom_list[1]))
            dicom_to_mat(option=2, root_path=dicom_list, output_path=output_path)
            zip_file_path = zip_files_from_folder(output_path, session_id)
            
            # zip_files_created_memory
            # https://stackoverflow.com/questions/27337013/how-to-send-zip-files-in-the-python-flask-framework
            # https://medium.com/analytics-vidhya/receive-or-return-files-flask-api-8389d42b0684
            
            return send_file(zip_file_path,
            mimetype = 'zip',
            attachment_filename= 'matlab_files.zip',
            as_attachment = True)
            
        if file_type == 'png':
            output_path = os.getcwd() + "\\vessel_app\data_saved\\png_session_id_{}".format(session_id)
            print(output_path)
            if os.path.exists(output_path):
                shutil.rmtree(output_path)
            dicom_data = Dicom.query.filter_by(session_id=session_id).first()
            dicom_list = query_to_dicom_list(dicom_data)
            dicom2png(dicom_list, output_path)
            zip_file_path = zip_files_from_folder(output_path, session_id)
            return send_file(zip_file_path,
            mimetype = 'zip',
            attachment_filename= 'png_files.zip',
            as_attachment = True)

        if file_type == 'jepg':
            pass

        if file_type == 'tiff':
            pass
        
        if file_type == 'jpeg_2000':
            pass

        if file_type == 'jpeg-ls':
            pass

        if file_type == 'RLE':
            pass

        if file_type == 'gif':
            pass


        # formData = DicomFormData(
        #     study_name=study_name,
        #     description=description,
        #     session_id=str(session['id']))
        # db.session.add(formData)
        # db.session.commit()
        # time.sleep(1.5)
        return redirect(url_for('file_pipeline.browser'))


        # data_3ds = Object_3D.query.filter_by(session_id=session_id).all()
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