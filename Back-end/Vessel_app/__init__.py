from flask import Flask

##logging imports
import logging
from vessel_app.flask_logs import LogSetup
from datetime import datetime as dt

# upload imports
from flask_dropzone import Dropzone
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class
import os

from flask_sqlalchemy import SQLAlchemy #URI SQLite database simply a file set as config file
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate
from vessel_app.config import Config # config class

app = Flask(__name__) ## Global Flask instance application Factory???


app.config.from_object(Config) # reference to config.py
## SQL database instance, classes or called 'models' 
db = SQLAlchemy(app)
migrate = Migrate(app, db)

bcrypt = Bcrypt(app)
dropzone = Dropzone(app)

## log info
app.config["LOG_TYPE"] = os.environ.get("LOG_TYPE", "stream")
app.config["LOG_LEVEL"] = os.environ.get("LOG_LEVEL", "INFO")
app.config['LOG_DIR'] = os.environ.get("LOG_DIR", "./")
app.config['APP_LOG_NAME'] = os.environ.get("APP_LOG_NAME", "app.log")
app.config['WWW_LOG_NAME'] = os.environ.get("WWW_LOG_NAME", "www.log")
logs = LogSetup()
logs.init_app(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

# Uploads settings
photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)
patch = patch_request_class(app) 

from vessel_app import routes, errors

