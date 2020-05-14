from flask_dropzone import Dropzone
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class
from flask_sqlalchemy import SQLAlchemy #URI SQLite database simply a file set as config file
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

from flask import Flask

app = Flask(__name__)

### CONFIGURATION REFERENCE
    #app.config.from_object('yourapplication.default_settings')
    #app.config.from_envvar('YOURAPPLICATION_SETTINGS')
    
app.config.from_object('vessel_app.config')
db = SQLAlchemy(app)

bcrypt = Bcrypt(app)
dropzone = Dropzone(app)
login_manager = LoginManager(app)

login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

# Uploads settings
photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)
patch = patch_request_class(app) 


from vessel_app import routes