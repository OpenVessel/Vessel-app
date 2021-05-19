import pickle
from vessel_app import db
from pydicom import dcmread
from pydicom.filebase import DicomBytesIO
from pydicom.charset import encode_string
from pydicom.datadict import dictionary_description as dd
import numpy as np
from vessel_app.models import User, Dicom, DicomFormData, Object_3D, Dicom2
from .vessel_pipeline_function import load_scan, get_pixels_hu, resample, sample_stack, make_lungmask, displayer, temp_file_db, pickle_vtk, make_lungmask_v2
from .utils import request_id

from vessel_app import create_celery_app
from celery.signals import task_prerun
from flask import g

#from vessel_app.file_pipeline.celery_tasks.data_pipeline import celery


# @task_prerun.connect
# def celery_prerun(*args, **kwargs):
#     #print g
#     with celery.app.app_context():
#         # use g.db
#         print(g)
    
#### celery -A vessel_app.celery worker -l info -P gevent
#### CELERY Task Queue block 
## celery -A vessel_app.file_pipeline.celery_tasks.celery worker --loglevel=info -P gevent
celery = create_celery_app()
@celery.task()
def data_pipeline(session_id, session_id_3d, n_clusters=2):
    
    ## Query database
    dicom_data = Dicom.query.filter_by(session_id=session_id).first()

    data = pickle.loads(dicom_data.dicom_stack)
    dicom_list = [] 
    for byte_file in data:
        dicom_list.append(dcmread(DicomBytesIO(byte_file)))
    
    #print(dicom_list) ## [FileDataSet, FileDataset, ..]
    ## STEP ONE of Masking pipeline 
    patient = load_scan(dicom_list) ## 3D array
    ## 
    print ("Slice Thickness: %f" % patient[0].SliceThickness)
    print ("Pixel Spacing (row, col): (%f, %f) " % (patient[0].PixelSpacing[0], patient[0].PixelSpacing[1]))

    ## STEP TWO of Masking pipeline
    image_stack = get_pixels_hu(patient)
    
    ## STEP THREE RESAMPLING
    print("Shape of CT slice before resampling", image_stack.shape)
    imgs_after_resamp, spacing = resample(image_stack, patient)
    print ("Shape after resampling\t", imgs_after_resamp.shape)

    masked_lung = []

    ## STEP FOUR K-MEANS MASKING
    for img in imgs_after_resamp: #loops through images and applies mask
        masked_lung.append(make_lungmask_v2(img, n_clusters=n_clusters))
    
    mask = np.array(masked_lung)
    ## pyvista
    data = displayer(mask)

    # convert pyvista class --> binary
    pickled_vtk = pickle_vtk(data)

## insert object into database calling class from model.py
    insert = Object_3D( 
        object_3D = pickled_vtk, 
        session_id=str(session_id),
        session_id_3d=str(session_id_3d)
        
    )
    
    db.session.add(insert) 
    db.session.commit()
    test = "I am done"
    return test

###
#### CELERY TASK CHAIN worksflows
####
## Serialization for JSON, DICOM, pickle, Query function to move database to another
@celery.task()
def query_db_insert(session_id):
    
    print("Query succesful")
    dicom_data = Dicom.query.filter_by(session_id=session_id).first()
    blob = dicom_data.dicom_stack
    
    insert = Dicom2(session_id=session_id ,
    dicom_stack=blob,
    )
    db.session.add(insert) 
    db.session.commit()
    #db.session.add(insert) 
    #db.session.commit()
    
    return "test done" ## this has return confirmation that the data was inserted 

### Load_data() pulls data from the database and lost objectt and returns the patient object 
@celery.task()
def load_data(session_id):
    ## Query database POSTGRES or 2nd_data
    dicom_data = Dicom.query.filter_by(session_id=session_id).first()
    
    ## seralizations 
    data = pickle.loads(dicom_data.dicom_stack)
    dicom_list = [] 
    for byte_file in data:
        dicom_list.append(dcmread(DicomBytesIO(byte_file)))
    
    ## Load_scan funcation is called form the pydicom package
    patient = load_scan(dicom_list) ## 3D array
    print ("Slice Thickness: %f" % patient[0].SliceThickness)
    print ("Pixel Spacing (row, col): (%f, %f) " % (patient[0].PixelSpacing[0], patient[0].PixelSpacing[1]))
    
    return patient ## the return result is patient is pushed to resampling 

## ## the resample  ##########
@celery.task()
def resample_task(patient):
    ## Query database
    
    ## STEP TWO of Masking pipeline
    image_stack = get_pixels_hu(patient)
    
    ## STEP THREE RESAMPLING
    print("Shape of CT slice before resampling", image_stack.shape)
    imgs_after_resamp, spacing = resample(image_stack, patient, [1,1,1])
    print ("Shape after resampling\t", imgs_after_resamp.shape)
    return imgs_after_resamp ## the return result is patient is pushed to resampling 

@celery.task()
def lung_segmentation(imgs_after_resamp):

    masked_lung = []
    ## STEP FOUR K-MEANS MASKING
    for img in imgs_after_resamp: #loops through images and applies mask
        masked_lung.append(make_lungmask_v2(img, n_clusters=n_clusters))
    
    mask = np.array(masked_lung)
    return mask ## the return result is patient is pushed to resampling


@celery.task()
def pyvista_call(mask):
    data = displayer(mask)
    ## the return result is patient is pushed to resampling
    ## pyvista
    # convert pyvista class --> binary
    pickled_vtk = pickle_vtk(data)

## insert object into database calling class from model.py
    insert = Object_3D( 
        object_3D = pickled_vtk, 
        session_id=str(session_id),
        session_id_3d=str(session_id_3d)
    )
    
    db.session.add(insert) 
    db.session.commit()
    return "I am done"