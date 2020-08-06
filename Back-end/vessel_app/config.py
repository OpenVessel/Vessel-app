## FLASK config class

#https://hackersandslackers.com/configure-flask-applications/\
#https://flask.palletsprojects.com/en/1.1.x/config/
#https://realpython.com/flask-by-example-part-1-project-setup/


import os
from flask import url_for
from os import environ, path
from dotenv import load_dotenv
basedir = os.path.abspath(os.path.dirname(__file__))
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(path.join(basedir,'.flaskenv'))

class Config:

    DEMO = False
    DEMO_EMAIL = 'sample@example.com'


    ########### Production config
    #SECRET_KEY = environ.get('SECRET_KEY')
    #FLASK_ENV = environ.get('FLASK_ENV')
    #FLASK_APP = 'wsgi.py'

    SECRET_KEY = 'ffb3986d5d75c04081caa3d7fb94c205'
    
    ###### DATABASE PATHING  ########### 
    #SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.getcwd() + r"\site.db"
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(os.getcwd(), "site.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False # we set this to false because flask-migrate will take care of this.


    ### Celery Workers ##########3
    CELERY_BROKER_URL='redis://localhost:6379/0'
    CELERY_RESULT_BACKEND='redis://localhost:6379/0'


    ########## reCAPtcha ########### 
    RECAPTCHA_USE_SSL= False
    RECAPTCHA_PUBLIC_KEY='6LdfyvsUAAAAAACFxPddYu-abcnVEf5lB_cKNbMo'
    RECAPTCHA_PRIVATE_KEY='6LdfyvsUAAAAAGS1HizHkCdkcQe5x8Gr8qPBWqIo'
    RECAPTCHA_OPTIONS= {'theme':'white'}


    ######## UPlOAD FOLDER (Need to be depcreated) #####
    UPLOADED_PHOTOS_DEST = os.getcwd() + 'static/uploads_files'
    ALLOWED_IMAGE_EXTENSIONS = {'dcm'}


    ####### Flask-Dropzone #######
    DROPZONE_ALLOWED_FILE_CUSTOM= True
    DROPZONE_IN_FORM=True
    DROPZONE_UPLOAD_ON_CLICK=True
    DROPZONE_UPLOAD_ACTION='file_pipeline.dropzone_handler'  # URL or endpoint
    DROPZONE_UPLOAD_BTN_ID='submit'
    DROPZONE_TIMEOUT=None

    ###### Logging #######
    LOG_TYPE = os.environ.get("LOG_TYPE", "stream")
    LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")
    LOG_DIR = os.environ.get("LOG_DIR", "./")
    APP_LOG_NAME = os.environ.get("APP_LOG_NAME", "app.log")
    WWW_LOG_NAME = os.environ.get("WWW_LOG_NAME", "www.log")