## FLASK config class

#https://hackersandslackers.com/configure-flask-applications/\
#https://flask.palletsprojects.com/en/1.1.x/config/
#https://realpython.com/flask-by-example-part-1-project-setup/


import os
from flask import url_for
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:

    ####### DATABASE SETTINGs ############
    SECRET_KEY = 'ffb3986d5d75c04081caa3d7fb94c205'
    
    ###### DATABASE PATHING 
    #SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:Sd40dash2@localhost/Vessel-test' 
    root_path = os.getcwd() 
    path = "sqlite:///" + root_path + r"\site.db"
    SQLALCHEMY_DATABASE_URI = path
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False # we set this to false because flask-migrate will take care of this.

    ### Celery Workers Config
    #CELERY_BROKER_URL='redis://localhost:6379/0'
    #CELERY_RESULT_BACKEND='redis://localhost:6379/0'


    ########## reCAPtcha ########### 

    RECAPTCHA_USE_SSL= False
    RECAPTCHA_PUBLIC_KEY='6LdfyvsUAAAAAACFxPddYu-abcnVEf5lB_cKNbMo'
    RECAPTCHA_PRIVATE_KEY='6LdfyvsUAAAAAGS1HizHkCdkcQe5x8Gr8qPBWqIo'
    RECAPTCHA_OPTIONS= {'theme':'white'}
    #FLASK_ENV = "development"


    ######## UPlOAD FOLDER Need to depcreated #####
    UPLOADED_PHOTOS_DEST = os.getcwd() + 'static/uploads_files'
    ALLOWED_IMAGE_EXTENSIONS = {'dcm'}

    # Flask-Dropzone config:
    DROPZONE_ALLOWED_FILE_CUSTOM= True
    DROPZONE_ALLOWED_FILE_TYPE='image/*, .dcm'
    DROPZONE_MAX_FILE_SIZE=3
    DROPZONE_MAX_FILES=400
    #DROPZONE_UPLOAD_MULTIPLE=False  
    #DROPZONE_PARALLEL_UPLOADS=10
    DROPZONE_IN_FORM=True
    DROPZONE_UPLOAD_ON_CLICK=True
    DROPZONE_UPLOAD_ACTION='dropzone_handler'  # URL or endpoint
    DROPZONE_UPLOAD_BTN_ID='submit'
    #DROPZONE_TIMEOUT =  300000

  