from vessel_app.file_pipeline.utils import pickle_vtk
from vessel_app.models import Dicom, Object_3D
from vessel_app import create_celery_app, db
from pydicom import dcmread

celery = create_celery_app()

class Drill:
    '''
        Base class to handle ML functions and their interactions with the database.
    '''
    def __init__(self, model_function, name='generic drill'):
        self.model_function = model_function
        self.name = name


    @celery.task()
    def query_dicom(self, session_id):
        '''
            Return a list of pydicom.dataset.FileDataset objects from the given session_id.

            session_id: str
        '''


        dicom_data = Dicom.query.filter_by(session_id=session_id).first()

        data = pickle.loads(dicom_data.dicom_stack)
        dicom_list = [] 
        for byte_file in data:
            dicom_list.append(dcmread(DicomBytesIO(byte_file)))

        return dicom_data


    @celery.task()
    def run_model_and_save(self, data, session_id_3d, *args, **kwawrgs):
        '''
            runs the function specified in the constructor of the drill and saves result to db under session_id_3d. Takes data (from a query function), session_id_3d, and any other args and kwargs.
            returns: done statement 

            data: list of pydicom.dataset.FileDataset objects
            session_id_3d: str
        '''
    

        pyvista_obj = self.model_function(data, *args, **kwargs)

        # convert pyvista obj --> binary
        pickled_vtk = pickle_vtk(pyvista_obj)

        ## insert object into database calling class from model.py
        insert = Object_3D( 
            object_3D = pickled_vtk, 
            session_id=session_id,
            session_id_3d=session_id_3d
            
        )
        
        db.session.add(insert) 
        db.session.commit()

        return f"Added pyvista obj to database at session_id_3d: {session_id_3d}"

    def __repr__(self):
        return f"<Drill ({self.name})>"
    
    __str__ = __repr__