from flask import Flask
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

login_manager = LoginManager(app)

login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

# Uploads settings
photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)
patch = patch_request_class(app) 

from vessel_app import routes, errors

