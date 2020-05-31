## FLASK config class

#https://hackersandslackers.com/configure-flask-applications/\
#https://flask.palletsprojects.com/en/1.1.x/config/
#https://realpython.com/flask-by-example-part-1-project-setup/


import os
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

    ########### DROPZONE #############

    # Dropzone settings
    UPLOAD_FOLDER = os.getcwd() + r'\vessel_app\static\uploads'
    DROPZONE_ALLOWED_FILE_TYPE='.dcm',
    DROPZONE_MAX_FILE_SIZE=20,
    DROPZONE_MAX_FILES=500,
    DROPZONE_PARALLEL_UPLOADS=500,  # set parallel amount
    DROPZONE_UPLOAD_MULTIPLE=True,  # enable upload multiple

    ########## reCAPtcha ########### 

    RECAPTCHA_USE_SSL= False
    RECAPTCHA_PUBLIC_KEY='6LdfyvsUAAAAAACFxPddYu-abcnVEf5lB_cKNbMo'
    RECAPTCHA_PRIVATE_KEY='6LdfyvsUAAAAAGS1HizHkCdkcQe5x8Gr8qPBWqIo'
    RECAPTCHA_OPTIONS= {'theme':'white'}



    ######## UPlOAD FOLDER Need to depcreated #####
    UPLOADED_PHOTOS_DEST = os.getcwd() + 'static/uploads_files'
    ALLOWED_IMAGE_EXTENSIONS = {'dcm'}