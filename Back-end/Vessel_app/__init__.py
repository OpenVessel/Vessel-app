from flask import Flask

##logging imports
import logging
from vessel_app.flask_logs import LogSetup
from datetime import datetime as dt

### Flask + Celery https://blog.miguelgrinberg.com/post/using-celery-with-flask
from celery import Celery

# flask app extensions
from flask_dropzone import Dropzone
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class
import os

from flask_sqlalchemy import SQLAlchemy #URI SQLite database simply a file set as config file
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate
from vessel_app.config import Config # config class

app = Flask(__name__) ## Global Flask instance application Factory???

## python-dot-env 

app.config.from_object(Config) # reference to config.py
## SQL database instance, classes or called 'models' 
db = SQLAlchemy(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
dropzone = Dropzone(app)

#### Flask + Celery 
app.config['CELERY_BROKER_URL'] = 'amqp://guest:guest@localhost:5672/' ## Input IP to direct messages to BROKER 
#app.config['CELERY_RESULT_BACKEND'] = 'amqp://guest:guest@localhost:5672/'
#app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/1'
app.config['CELERY_RESULT_BACKEND'] = 'rpc://'

 ### response will be sent back to RabbitMQ queue 

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL']) ## Celery is initialized by obj class Celery
#celery.conf.update(app.config) for some reason causes a igorne 

## log info
app.config["LOG_TYPE"] = os.environ.get("LOG_TYPE", "stream")
app.config["LOG_LEVEL"] = os.environ.get("LOG_LEVEL", "INFO")
app.config['LOG_DIR'] = os.environ.get("LOG_DIR", "./")
app.config['APP_LOG_NAME'] = os.environ.get("APP_LOG_NAME", "app.log")
app.config['WWW_LOG_NAME'] = os.environ.get("WWW_LOG_NAME", "www.log")
logs = LogSetup(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

# Uploads settings
photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)
patch = patch_request_class(app) 

from vessel_app import routes, errors

