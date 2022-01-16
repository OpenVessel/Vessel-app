## FLASK config class

#https://hackersandslackers.com/configure-flask-applications/\
#https://flask.palletsprojects.com/en/1.1.x/config/
#https://realpython.com/flask-by-example-part-1-project-setup/


import os
from flask import url_for
from os import environ, path
from dotenv import load_dotenv


basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(path.join(basedir,'.flaskenv'))

class Config:

    ## CORS CONFIG
    CORS_ALLOW_HEADERS: "*"
    CORS_ALWAYS_SEND: True
    CORS_AUTOMATIC_OPTIONS: True
    CORS_EXPOSE_HEADERS: None
    CORS_INTERCEPT_EXCEPTIONS: True
    CORS_MAX_AGE: None
    CORS_METHODS: ["GET", "HEAD", "POST", "OPTIONS", "PUT", "PATCH", "DELETE"]
    CORS_ORIGINS: "*" # Origins? 
    CORS_RESOURCES: r"/*"
    CORS_SEND_WILDCARD: False
    CORS_SUPPORTS_CREDENTIALS: True
    CORS_VARY_HEADER: True


    ###### Logging #######
    LOG_TYPE = os.environ.get("LOG_TYPE", "stream")
    LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")
    LOG_DIR = os.environ.get("LOG_DIR", "./")
    APP_LOG_NAME = os.environ.get("APP_LOG_NAME", "app.log")
    WWW_LOG_NAME = os.environ.get("WWW_LOG_NAME", "www.log")
