import os
from flask import Flask, request, jsonify, url_for, Blueprint, render_template, send_from_directory, current_app
from . import bp
from .utils import generate_sitemap, APIException
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required

# from .models import db
# from .admin import setup_admin
from vessel_app.models import User

ENV = os.getenv("FLASK_ENV")
static_file_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'templates\\')
print(static_file_dir)

# generate sitemap with all your endpoints
@bp.route('/', methods=['POST', 'GET'])
def sitemap():
    ## this generates site map when we do http://127.0.0.1:5000/api/ in the browser 
    if ENV == "development":
        return generate_sitemap(current_app)
    
    ## we want API accessible during productions needs  dev work
    if ENV == "production":
        pass
    return send_from_directory(static_file_dir, 'test_api.html')

# Handle/serialize errors like a JSON object
@bp.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# any other endpoint will try to serve it like a static file
@bp.route('/<path:path>', methods=['GET'])
def serve_any_other_file(path):
    if not os.path.isfile(os.path.join(static_file_dir, path)):
        path = 'test_api.html'
    response = send_from_directory(static_file_dir, path)
    response.cache_control.max_age = 0 # avoid cache memory
    return response

# 127.0.0.1/api/token
@bp.route('/token', methods=['POST'])
def create_token(): 
    print("we receviced a request")
    email = request.json.get("email", None)
    password = request.json.get("password", None)

    if email != "test" or password != "test":
        return jsonify({"msg": "Bad username or password"}), 401

    access_token = create_access_token(identity=email)
    return jsonify(access_token=access_token), 200

# machine learning its goes to anothe database or server