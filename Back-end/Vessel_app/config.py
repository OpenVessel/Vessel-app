## FLASK config class

#https://hackersandslackers.com/configure-flask-applications/\
#https://flask.palletsprojects.com/en/1.1.x/config/
#https://realpython.com/flask-by-example-part-1-project-setup/


import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:

    ####### DATABASE SETTINGs ############
    SECRET_KEY = 'ffb3986d5d75c04081caa3d7fb94c205'
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:Sd40dash2@localhost/Vessel-test' 
   

    ########### DROPZONE #############

    UPLOADED_PATH=os.path.join(basedir, 'uploads')
    # Flask-Dropzone config:
    DROPZONE_ALLOWED_FILE_CUSTOM=True
    DROPZONE_ALLOWED_FILE_TYPE='.dcm'
    DROPZONE_MAX_FILE_SIZE=5
    DROPZONE_MAX_FILES=20
    DROPZONE_UPLOAD_ON_CLICK=True
    DROPZONE_UPLOAD_MULTIPLE=True
    DROPZONE_PARALLEL_UPLOADS = 3 
  
