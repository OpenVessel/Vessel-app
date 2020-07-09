from flask import Flask, current_app

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

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate
from vessel_app.config import Config

db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
dropzone = Dropzone()
login_manager = LoginManager()
logs = LogSetup()
celery = Celery()
def create_app(config_class=Config):

    app = Flask(__name__) ## Global Flask instance application Factory???

    app.config.from_object(Config) # reference to config.py
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    dropzone.init_app(app)
    

    # blueprint registrations
    from .blueprints.errors import bp as errors_bp
    app.register_blueprint(errors_bp)
    from .blueprints.auth import bp as auth_bp
    app.register_blueprint(auth_bp)
    from .blueprints.main import bp as main_bp
    app.register_blueprint(main_bp)
    from .blueprints.file_pipeline import bp as file_pipeline_bp
    app.register_blueprint(file_pipeline_bp)

    #celery -A vessel_app.celery worker -l info -P gevent

    # def make_celery(app):
    #     celery = Celery(
    #         app.import_name,
    #         backend=app.config['CELERY_RESULT_BACKEND'],
    #         broker=app.config['CELERY_BROKER_URL']
    #     )
    #     #celery.conf.update(app.config) what is this config?>

    #     class ContextTask(celery.Task):
    #         def __call__(self, *args, **kwargs):
    #             with app.app_context():
    #                 return self.run(*args, **kwargs)

    #     celery.Task = ContextTask
    #     return celery

    # celery = make_celery(current_app)
    # celery = make_celery(app)

    ## log info
    app.config["LOG_TYPE"] = os.environ.get("LOG_TYPE", "stream")
    app.config["LOG_LEVEL"] = os.environ.get("LOG_LEVEL", "INFO")
    app.config['LOG_DIR'] = os.environ.get("LOG_DIR", "./")
    app.config['APP_LOG_NAME'] = os.environ.get("APP_LOG_NAME", "app.log")
    app.config['WWW_LOG_NAME'] = os.environ.get("WWW_LOG_NAME", "www.log")
    logs.init_app(app)

    login_manager.init_app(app)
    login_manager.login_view = 'login'
    login_manager.login_message_category = 'info'

    # Uploads settings
    photos = UploadSet('photos', IMAGES)
    configure_uploads(app, photos)
    patch = patch_request_class(app) 

    return app

def create_celery_app(app=None):
        app = app or create_app(Config)
        celery = Celery(__name__, 
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL'])
        celery.conf.update(app.config)
        TaskBase = celery.Task

        class ContextTask(TaskBase):
            abstract = True

            def __call__(self, *args, **kwargs):
                with app.app_context():
                    return TaskBase.__call__(self, *args, **kwargs)

        celery.Task = ContextTask
        return celery