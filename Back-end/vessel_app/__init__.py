from flask import Flask, current_app
from flask import send_from_directory

##logging imports
import logging
from datetime import datetime as dt

### Flask + Celery https://blog.miguelgrinberg.com/post/using-celery-with-flask
from celery import Celery
# flask app extensions
from flask_dropzone import Dropzone
from flask_uploads import UploadSet, configure_uploads, IMAGES
import os

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate
from vessel_app.config import Config

from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with

db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
dropzone = Dropzone()
login_manager = LoginManager()
jwt = JWTManager()
cors = CORS()
api = Api()
# logs = LogSetup()
celery = Celery(__name__, broker=Config.CELERY_BROKER_URL)


## AUTOMATE THE REDIS db.create_all tables functionlity
# os.system("python script.py ")
# os.system("from multiple_databases import db")
# os.system("db.create_all(bind=['redis_db'])")
# os.system("python")
def create_app(config_class=Config):

    # https://owasp.org/www-project-top-ten/
    root_path = os.getcwd()
    instance_path = root_path + "\\user_3d_objects"
    app = Flask(__name__, instance_path = instance_path) ## Global Flask instance application Factory???
    app.config.from_object(Config) # reference to config.py
    db.init_app(app)
    api.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    dropzone.init_app(app)
    celery.conf.update(app.config)
    jwt.init_app(app)
    cors.init_app(app, supports_credentials=True )
    # logs.init_app(app)

    login_manager.init_app(app)
    login_manager.login_view = 'login'
    login_manager.login_message_category = 'info'

    # profile uploads settings (Deprecate)
    photos = UploadSet('photos', IMAGES)
    configure_uploads(app, photos)
    
    
    with app.app_context():
        # blueprint registrations
        from .errors import bp as errors_bp
        app.register_blueprint(errors_bp)
        from .auth import bp as auth_bp
        app.register_blueprint(auth_bp)
        from .main import bp as main_bp
        app.register_blueprint(main_bp)
        from .file_pipeline import bp as file_pipeline_bp
        app.register_blueprint(file_pipeline_bp)
        from .browser import bp as browser_bp
        app.register_blueprint(browser_bp)
        from .submit_job import bp as submit_job_bp
        app.register_blueprint(submit_job_bp)
        from .viewer_3d import bp as viewer_3d_bp
        app.register_blueprint(viewer_3d_bp)
        from .conversion_code import bp as conversion_code_bp
        app.register_blueprint(conversion_code_bp)
        from .global_api import bp as global_api_bp
        app.register_blueprint(global_api_bp, url_prefix='/api')

        # flask + react # Last resort
        # https://www.youtube.com/watch?v=YW8VG_U-m48


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