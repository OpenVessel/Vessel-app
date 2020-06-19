import pickle
from vessel_app import  db, celery
from pydicom import dcmread
from pydicom.filebase import DicomBytesIO
from pydicom.charset import encode_string
from pydicom.datadict import dictionary_description as dd
import numpy as np
from vessel_app.models import User, Dicom, DicomFormData, Object_3D
from vessel_app.vessel_pipeline_function import load_scan, get_pixels_hu, resample, sample_stack, make_lungmask, displayer, temp_file_db, pickle_vtk

#### celery -A vessel_app.celery worker -l info -P gevent
#### CELERY Task Queue block 
@celery.task()
def data_pipeline(session_id, b):
    
    # ESSENTIAL IMPORTS
    #import numpy as np
    ## vessel functions 
    #from vessel_app.vessel_pipeline_function import load_scan, get_pixels_hu, resample, sample_stack, make_lungmask

    b = b
    
    dicom_data = Dicom.query.filter_by(session_id=session_id).first()

    data = pickle.loads(dicom_data.dicom_stack)
    dicom_list = [] 
    for byte_file in data:
        dicom_list.append(dcmread(DicomBytesIO(byte_file)))
    
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
    
    mask = np.array(masked_lung)
    data = displayer(mask)

    # convert pyvista class --> binary
    pickled_vtk = pickle_vtk(data)
    
    string_ok = "test"
    insert = Object_3D( 
    object_3D = pickled_vtk, 
    session_id=str(session_id),
    test = str(string_ok)
    )
    
    db.session.add(insert) 
    db.session.commit()

    return 
