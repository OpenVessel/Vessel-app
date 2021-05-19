import os
import shutil
from flask_login import current_user, login_required, login_user
from flask import render_template, url_for, flash, redirect, request, session, after_this_request, current_app, Response
from .utils import request_id, dicom_to_thumbnail
from .celery_tasks import data_pipeline, query_db_insert, load_data, lung_segmentation, pyvista_call, query_db_insert, resample
from vessel_app.models import User, Dicom, DicomFormData, Object_3D

from .celery_tasks import data_pipeline, query_db_insert, load_data, lung_segmentation, pyvista_call, query_db_insert, resample
from .utils import request_id, dicom_to_thumbnail
from .vessel_pipeline_function import load_scan, get_pixels_hu, resample, sample_stack, make_lungmask, displayer, temp_file_db, pickle_vtk, unpickle_vtk, unpickle_vtk_2
from . import bp

@bp.before_app_request
def before_fun():
    internal_endpoints = [rule.endpoint for rule in current_app.url_map.iter_rules()]
    #print(internal_endpoints)
    try:
        print("Output before -------- ",session['last_endpoint'])
    except:
        session['last_endpoint'] = 'nowhere'
        print("Output before -------- ",session['last_endpoint'])
    
    if current_user.is_authenticated and request.endpoint =='file_pipeline.upload':

        # create session_id
        session['id'] = request_id()
        print('SESSION_ID before request:', session['id'])


    if current_user.is_authenticated and session['last_endpoint'] == 'viewer_3d.viewer_3d' and request.endpoint != 'static' and request.endpoint in internal_endpoints:
        print('just left 3d viewer')
        # BUG: WONT DELETE FILES IF THE USER LEAVES THE SITE FROM 3D VIEWER
        if os.path.isdir(session['path_3d']):
            # remove user folder

            print('removing files')
            shutil.rmtree(session['path_3d'])


@bp.route('/3d_viewer', methods=['POST'])
def viewer_3d():

    source = request.form.get('source')

    # you should only get here from browser and job submit
    if source not in ['browser', 'job_submit']:
        redirect(url_for('file_pipeline.browser'))


    # update path_3d
    temp_dir = os.path.join(os.getcwd(), "vessel_app", "static", "users_3d_objects" )
    temp_user_dir = "user_" + str(current_user.id)
    session['path_3d'] = os.path.join(temp_dir, temp_user_dir)

    if not os.path.isdir(session['path_3d']):
        os.mkdir(path = session['path_3d'])

    print('getting object_3d from folder:', session['path_3d'])

    print(f'Generating model from {source}')


    if source == 'job_submit':
        # get request data
        session_id = request.form.get('session_id')
        k = int(request.form.get('k'))
        segmentation_options = request.form.get("segmentation_options") # blood, bone, etc.

        # create a session_id_3d
        session_id_3d = str(request_id())

        # Call worker and save result to database
        result = data_pipeline.delay(session_id, session_id_3d, n_clusters=k)
        result_output = result.wait(timeout=None, interval=0.5)

        #test_data = load_data.delay(session_id)            
        #print(test_data)

        ## WORKER CALL CHain workflow
        # celery.chain(query_db_insert() , 
        # load_data(),
        # resample(),
        # lung_segmentation(),
        # pyvista_call(), 
        
        # ).apply()    

        
    elif source == "browser":
        session_id_3d = request.form.get('session_id_3d')

    # query database for object_3D
    data = Object_3D.query.filter_by(session_id_3d=session_id_3d).first()
    data_as_pyvista_obj = unpickle_vtk(data.object_3D)

    # save to .vti file
    object_3d_path = os.path.join(session['path_3d'], "data_object.vti")


    data_as_pyvista_obj.save(object_3d_path)
    print(object_3d_path)
    object_3d_path = os.path.relpath(object_3d_path, start = "vessel_app")
    print(object_3d_path)
    object_3d_path = object_3d_path.replace("\\", "/")
    

    return render_template('3d_viewer.html', path_data=object_3d_path)