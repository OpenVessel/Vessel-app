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
    
    #SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    #SQLALCHEMY_DATABASE_URI = r'sqlite:///C:\Users\grego\Documents\GitHub\Vessel-app\Back-end\site.db'
    SQLALCHEMY_DATABASE_URI = r'sqlite:///D:\Openvessel\vessel-app\Back-end\site.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False # we set this to false because flask-migrate will take care of this.

    ########## reCAPtcha ########### 

    RECAPTCHA_USE_SSL= False
    RECAPTCHA_PUBLIC_KEY='6LdfyvsUAAAAAACFxPddYu-abcnVEf5lB_cKNbMo'
    RECAPTCHA_PRIVATE_KEY='6LdfyvsUAAAAAGS1HizHkCdkcQe5x8Gr8qPBWqIo'
    RECAPTCHA_OPTIONS= {'theme':'white'}



    ######## UPlOAD FOLDER Need to depcreated #####
    UPLOADED_PHOTOS_DEST = os.getcwd() + 'static/uploads_files'
    ALLOWED_IMAGE_EXTENSIONS = {'dcm'}

    # Flask-Dropzone config:
    DROPZONE_ALLOWED_FILE_CUSTOM= True
    DROPZONE_ALLOWED_FILE_TYPE='image/*, .dcm'
    DROPZONE_MAX_FILE_SIZE=3
    DROPZONE_MAX_FILES=30
    DROPZONE_IN_FORM=True
    DROPZONE_UPLOAD_ON_CLICK=True
    DROPZONE_UPLOAD_ACTION='upload'  # URL or endpoint
    DROPZONE_UPLOAD_BTN_ID='submit'