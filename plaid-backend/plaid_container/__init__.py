from flask import Flask, current_app
from flask import send_from_directory
import os
from flask_bcrypt import Bcrypt
from plaid_container.config import Config
from flask_cors import CORS

bcrypt = Bcrypt()
cors = CORS()


def create_app(config_class=Config):

    # https://owasp.org/www-project-top-ten/
    root_path = os.getcwd()
    instance_path = root_path + "\\user_3d_objects"
    
    app = Flask(__name__, instance_path = instance_path) ## Global Flask instance application Factory???
    app.config.from_object(Config) # reference to config.py
    bcrypt.init_app(app)
    cors.init_app(app, supports_credentials=True )
    
    
    with app.app_context():
        # blueprint registrations
        from .plaidApi import bp as plaidApi_bp
        app.register_blueprint(plaidApi_bp)

        return app
