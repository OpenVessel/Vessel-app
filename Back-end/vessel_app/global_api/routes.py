import os
import requests
from flask import Flask, request, jsonify, url_for, Blueprint, render_template, send_from_directory, current_app, session
from .security import validate_header
from . import bp
from .utils import generate_sitemap, APIException, password_check
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required

from vessel_app import db, bcrypt
from flask_cors import CORS, cross_origin
# Form dataclasses 
from .forms import  RegistrationForm, LoginForm, UpdateAccountForm, SessionBasedForm
from wtforms import Form, BooleanField, StringField, validators
from wtforms.csrf.core import CSRF
# from wtforms.csrf.session import SessionCSRF
# from .models import db
# from .admin import setup_admin
from flask_login import login_user, current_user, logout_user, login_required
from vessel_app.models import User, ContactInfo, Verify
from .connector_redis import save_csrf, check_csrf_token
## routes are for your endpoints

## Request notes
# print(request.headers)
# # print(request.data)
# # print(request.args)
# # print(request.form)
# # print(request.endpoint)
# # print(request.remote_addr)

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
@bp.route('/login_call', methods=['POST'])
def create_token(): 

    print("we receviced a request from", request.remote_addr)
    username = request.json.get("username", None)
    email = request.json.get("email", None)
    password = request.json.get("password", None)

    if request.method == 'POST':
        ## we take the json values out of the HTTPS request
        print("hellloooooofrom react")
        ## we pass them to user.query.filter
        ## we need validation code for email 
        username_pass = username
        password_pass = password
        print("username ",username_pass)
        print("password",password_pass)
        ## Input validation authen
        ## we pull the password withthe user name or email
        user = User.query.filter_by(username=username_pass).first()
            
        # Validate if user exist 
        print(bcrypt.check_password_hash(user.password, password))
        print(username == user.username)
        print(username != user.username)
        if username != user.username:
            return jsonify({"msg": "Bad username"}), 401
            #     email = StringField('Email', # does email exist?
            # password = PasswordField('Password', validators=[DataRequired()]) ## password exist is it correct does sit match
            # remember = BooleanField('Remember Me')
            # submit = SubmitField('Login')
            # recaptcha = RecaptchaField()
        print(user)
        ## we check the hash generated on the password
        if  bcrypt.check_password_hash(user.password, password):
            # https://flask-login.readthedocs.io/en/latest/
            #  https://flask-login.readthedocs.io/en/latest/#flask_login.login_user
            did_user_login = login_user(user)
            
            if did_user_login == True: 
                ## if login_user returns true we pass the token and redirect trigger to account page to displaye user naem
                access_token = create_access_token(identity=email)
                response_pay_load = {  
                    "message":"Successful Login",
                    "username":user.username,
                    "email":user.email,
                    "access_token":access_token
                            }

                return jsonify(response_pay_load), 200
            else:
                response_pay_load = {  "message":"Login Unsuccessful. Please check username and password"  }
            return jsonify(response_pay_load), 200

        else:
            response_pay_load = {  "message":"Login Unsuccessful. Please check username and password"  }
            return jsonify(response_pay_load), 200



# 127.0.0.1/api/upload
@bp.route('/upload_call', methods=['POST'])
def upload_call(): 
    return jsonify(), 200


# 127.0.0.1/api/browser
@bp.route('/browser_call', methods=['POST'])
def browser_call(): 
        ## returns a list of data to the browser to the 
    ## user 
    return jsonify(), 200


# crsf_token_call
@bp.route('csrf_token_call', methods=['GET'])
# @cross_origin() ## need to change code on flux.js to recevie this function
def create_csrf_token():
    print("its a  wr",request.method)
    header = request.headers
    ## Sercuity function  prevent CSRF attacks 
    validate_header(header)
    ## when client opens the browser generates a CSRF token that is load into local session that auto fills all hidden tags
    form = SessionBasedForm()

    if request.method == 'GET':
        csrf_token = form.csrf_token
        ## so we created a token 
        print(csrf_token.current_token)
        token_passing = csrf_token.current_token
        token_id = save_csrf(token_passing) ## we save token for 45 minutes into redis database for caching 
        print(token_id)
        check_obj = check_csrf_token(token_id, True)
        
        if token_passing == check_obj:
            print("Preflight check", token_passing == check_obj)
        

    return jsonify(data=token_passing, token_id=token_id, success=True)

# 127.0.0.1/api/browser
@bp.route('/contactInfo', methods=['POST','GET'])
def contactInfo(): 
    json_obj = request.json
    token_id = json_obj['token_id']
    username_pass = json_obj['username']
    user = User.query.filter_by(username=username_pass).first()

    if request.method == 'POST':
        token = check_csrf_token(token_id, True)
        if json_obj['csrf_token'] == token:
            print("Tokens Match approved")
            print(request.json)


            phonenumber = json_obj['phonenumber']
            residentialaddress = json_obj['residentialaddress']
            city = json_obj['city']
            zipcode = int(json_obj['zipcode'])
            submit = json_obj['submit']
            print(phonenumber)
            print(residentialaddress)
            print(city)
            print(zipcode)
            print(user.id)



            if submit == 'ContactInfo':
                print("hello?")
                contactinfo = ContactInfo(
                    user_id=user.id,
                    username=username_pass,
                    phonenumber=phonenumber,
                    residentialaddress=residentialaddress,
                    city=city,
                    zipcode=zipcode
                )
                db.session.add(contactinfo)
                
                try:
                    db.session.commit()
                    print('ContactInfo has been created! You are now able to log in', 'success')
                    response_pay_load = { 
                        
                        "message":"ContactInfo, You are now able to log in",
                        "username":username_pass,
                        }
                    
                    return jsonify(response_pay_load), 200
                
                except:
                    print("SQL insert failed")
                    response_pay_load = { 
                        "message":"Failed to commit data to the database for ContactInfo"
                        }
                    return jsonify(response_pay_load), 200

                
            else:
                print("failed to validate or create a account")
                response_pay_load = { 
                    "message":"failed to validate or create a account ContactInfo"
                    }
                return jsonify(response_pay_load), 200


# 200	OK
# 400	BAD REQUEST
# 401	UNAUTHORIZED
# 403	FORBIDDEN
# 404	NOT FOUND
# 417	EXPECTATION FAILED
# 500	INTERNAL SERVER ERROR

@bp.route('/Verification', methods=['POST','GET'])
def Verification(): 
    json_obj = request.json
    token_id = json_obj['token_id']
    # username_pass = json_obj['username']
    username_pass = 'test'
    print(username_pass)
    user = User.query.filter_by(username=username_pass).first()

    if request.method == 'POST':
        token = check_csrf_token(token_id, True)
        if json_obj['csrf_token'] == token:
            print("Tokens Match approved")
            print(request.json)


        # "token_id":token_id,
		# 				"csrf_token":csrf_token,
		# 				"username":username,
		# 				"ssn":ssn, 
		# 				"DOB":DOB,						
		# 				"citizenship":citizenship,						
		# 				"submit":"Verification"
        ## bcrypt 
            ssn = json_obj['ssn']
            citizenship = json_obj['citizenship']
            DOB = json_obj['DOB']
            submit = json_obj['submit']
            print(ssn)
            print(citizenship)
            print(DOB)
            print(user.id)
            pass_id = user.id
            if submit == 'Verification':
                print("hello?")
                
                print("hello?")
                # db.session.add(dbVerify)
                # db.session.commit()
                Verify(username=username_pass, ssn=ssn, dob=DOB, citizenship=citizenship)

                try:
                    db.session.commit()
                    print('Verification has been created! You are now able to log in', 'success')
                    response_pay_load = { 
                        
                        "message":"Verification, You are now able to log in",
                        "username":username_pass,
                        }
                    
                    return jsonify(response_pay_load), 200
                
                except:
                    print("SQL insert failed")
                    response_pay_load = { 
                        "message":"Failed to commit data to the database for Verification"
                        }
                    return jsonify(response_pay_load), 200

                
            else:
                print("failed to Verification")
                response_pay_load = { 
                    "message":"failed to validate or create a account Verification"
                    }
                return jsonify(response_pay_load), 200

## Ankr 
## Eth 
## https://apis.ankr.com/332b544115a14ccfb34df2d597d39207/b7b94fefa553f7c5f61f4736bd8a49d6/eth/fast/main

# 127.0.0.1/api/heloo
# So only people with appended token into the request will access the function
@bp.route('/hello', methods=['GET'])
@jwt_required()
def get_hello(): 

    # python dict
    json = { 
        "message":"hello world"
    }
    return jsonify(json), 200


## registration via API 
@bp.route("/register", methods=['GET', 'POST'])
def register():

    print("test request", request.method)
    json_obj = request.json
    ## we call check_csrf see if it existing if not deined request
    ## if it does exist go on to form registration to automatically past csrf to 
    if request.method == 'POST':
        print("someone is registering checking csrf cache")
        token_id = json_obj['token_id']
        token = check_csrf_token(token_id, True)
        
        if json_obj['csrf_token'] == token:
            print("Tokens Match approved")
            print(request.json)

            username = json_obj['username']
            email = json_obj['email']
            password = json_obj['password']
            firstname = json_obj['firstname']
            lastname = json_obj['lastname']
            confirmpassword = json_obj['confirm_password']
            submit = json_obj['submit']
            

            print("------",request.form)
            
            if request.method == 'POST':
                ## hashed password
                ## fails to check if passwords match!!!
                user = User.query.filter_by(username=username).first()

                if user:
                    print("username already exist")

                user = User.query.filter_by(email=email).first()
            
                if user:
                    print("email already exist")

                hashed_password = bcrypt.generate_password_hash(password).decode('utf-8') 
                
                user = User(
                    username=username, 
                    email=email, 
                    password=hashed_password, 
                    lastname=lastname,
                    firstname=firstname
                    ) 

                db.session.add(user)
                try:
                    db.session.commit()
                    print('Your account has been created! You are now able to log in', 'success')
                    response_pay_load = { 
                        
                        "message":"Your account has been created! You are now able to log in",
                        "firstname":firstname,
                        "username":username
                        }
                    
                    return jsonify(response_pay_load), 200
                
                except:
                    print("SQL insert failed")
                    
                    response_pay_load = { 
                        
                        "message":"Failed to commit data to the database"

                        }
                    
                    
                    return jsonify(response_pay_load), 200

                
            else:
                print("failed to validate or create a account")
                response_pay_load = { 
                    "message":"failed to validate or create a account"
                    }
                return jsonify(response_pay_load), 200

import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials


@bp.route('/google_api_call')
def google_api_call():
    API = process.env.GOOGLEAPIKEY
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

##
## polygon calls
def polygon_call_api():
    return


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


@bp.route("/account",  methods=['GET', 'POST'])
def account():

    print("test request", request.method)
    json_obj = request.json
    print(json_obj)

    username = json_obj['username']
    email = json_obj['email']
    password = json_obj['password']
    confirmpassword = json_obj['confirm_password']
    submit = json_obj['submit']

    if request.method == 'POST':
        print("user is changing account checking csrf cache")
        token_id = json_obj['token_id']
        token = check_csrf_token(token_id, True)
        print(token)
        
        if json_obj['csrf_token'] == token:

            change_user = User.query.filter_by()

            admin = User.query.filter_by(username='admin').first()
            admin.email = 'my_new_email@example.com'
            db.session.commit()

            user = User.query.get(5)
            user.name = 'New Name'
            db.session.commit()

        ## did usuer change emaiL? 
        ## did user change username?
        # picture data uploaded  passed to
            if form.picture.data:
                ## we extract image 
                image_data = request.files[form.picture.name].read()
                img_obj = Image.open(BytesIO(image_data))

                # save bytes image to database
                img_bytes = BytesIO()
                img_obj.save(img_bytes, format='PNG')
                img_bytes = img_bytes.getvalue()
                current_user.image_file = img_bytes

            current_user.username = form.username.data
            current_user.email = form.email.data
            db.session.commit()
            flash('Your account has been updated!', 'success')
            return redirect(url_for('auth.account'))
        elif request.method == 'GET':
            form.username.data = current_user.username
            form.email.data = current_user.email

            print('getting user image')
            img_bytes = current_user.image_file

            if not img_bytes:
                print('no image')
                # no profile image
                default_image_dir = str(os.getcwd()) + r'/vessel_app/static/img/default_user.png'
                img_obj = Image.open(default_image_dir)
                img_bytes = BytesIO()
                img_obj.save(img_bytes, format='PNG')
                img_bytes = img_bytes.getvalue()
            
            
            raw_image = BytesIO(img_bytes).read()  
            profile_image = b64encode(raw_image).decode('ascii')

        return render_template('account.html', title='Account', image_file=profile_image, form=form)




