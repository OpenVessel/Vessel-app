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
## routes are for your endpoints

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

    print("we receviced a request from")
    email = request.json.get("email", None)
    password = request.json.get("password", None)

    if email != "test" or password != "test":
        return jsonify({"msg": "Bad username or password"}), 401

    access_token = create_access_token(identity=email)
    return jsonify(access_token=access_token), 200


import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials


@bp.route('/google_api_call')
def google_api_call():
    API_KEY = "AIzaSyBI4_jfbJcd6LhYFJWf0clTYlja6mYyS9Y"
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """

    # If modifying these scopes, delete the file token.json.
    SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('drive', 'v3', credentials=creds)

    # Call the Drive v3 API
    results = service.files().list(
        pageSize=10, fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])

    if not items:
        print('No files found.')
    else:
        print('Files:')
        for item in items:
            print(u'{0} ({1})'.format(item['name'], item['id']))
    
    return "pass"

# machine learning its goes to anothe database or server

##
## After step 25th we are intergrating into existing medical software platforms 
##Epic's APi 
## #https://fhir.epic.com/Documentation?docId=developerguidelines



#### API query for HL7 
## ingestion framework 
# message = 'MSH|^~\&|GHH LAB|ELAB-3|GHH OE|BLDG4|200202150930||ORU^R01|CNTRL-3456|P|2.4\r'
# message += 'PID|||555-44-4444||EVERYWOMAN^EVE^E^^^^L|JONES|196203520|F|||153 FERNWOOD DR.^^STATESVILLE^OH^35292||(206)3345232|(206)752-121||||AC555444444||67-A4335^OH^20030520\r'
# message += 'OBR|1|845439^GHH OE|1045813^GHH LAB|1554-5^GLUCOSE|||200202150730||||||||555-55-5555^PRIMARY^PATRICIA P^^^^MD^^LEVEL SEVEN HEALTHCARE, INC.|||||||||F||||||444-44-4444^HIPPOCRATES^HOWARD H^^^^MD\r'
# message += 'OBX|1|SN|1554-5^GLUCOSE^POST 12H CFST:MCNC:PT:SER/PLAS:QN||^182|mg/dl|70_105|H|||F'
# import hl7 
# test = hl7.parse(message)
# print(test)
# print(type(test))
# print(test[1])
#https://help.interfaceware.com/getting-sample-hl7-data.html
#http://www.ringholm.com/docs/04300_en.htm
#https://blog.interfaceware.com/components-of-an-hl7-message/
#http://www.ringholm.com/training/FHIR_training_course.htm
#https://www.ihe.net/
#https://www.dicomstandard.org/
#https://github.com/firelyteam/fhir-net-api
#http://docs.simplifier.net/fhirnetapi/
#https://github.com/firelyteam/fhir-net-api
#