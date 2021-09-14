
import os
from os import environ, path
from dotenv import load_dotenv
import json
import requests
import numpy as np
from vessel_app.models import UserReact, ContactInfo, Verify, Checkpoint, AuthTable
# basedir = os.path.abspath(os.path.dirname(__file__))
basedir = r'D:\L_pipe\vessel_app_celery\Vessel-app\Back-end'
pathtoenv = path.join(basedir,'.flaskenv')
print(pathtoenv)
load_dotenv(pathtoenv)

## Call company API key from Authenticating SDK 
AUTHKEY = os.environ.get("AUTH_COMPANY_ADMIN_KEY_GOES_HERE")
print(AUTHKEY)

## Core parameter is username
## CreateAccessCode reutrn code to insert
## Sumbit UserConset with AccessCode 
##

def CreateAccessCode(username, mockAPI):

    #
    if mockAPI == True:

        # fake mockAPI
        appDict = {
        "firstName":"Jonathan",
        "middleName":"Gob",
        "lastName":"Zinx",
        "dob":"22-05-1990",
        "email":"jonathan@authenticating.com",
        "houseNumber":"504",
        "streetName":"121, 9th ST",
        "address":"121, 9th ST, APT 12111",
        "city":"Santa Monica",
        "state":"CA",
        "zipCode":"90411"
        }

        headers = {
        'content-type': 'application/json',
        }

        print(headers)
        resp = requests.post(url = 'https://api-v3-stage.authenticating.com/mock/user/create', headers=headers, json=appDict)
        print(resp)

        if resp.status_code == 200:
            statement = resp.json()
            print(statement)

            #imagine we insert data into datatable AuthenticateTable

    # Produciton
    if mockAPI == False:
        
        #every time this function is called its pararmeter is username and MockAPI = False
        username=username
        UserQuery = UserReact.query.filter_by(username=username).first()
        ContactInfoQuery = ContactInfo.query.filter_by(username=username).first()
        VerifyQuery = Verify.query.filter_by(username=username).first()
        
        # FirstName, LastName, DateOfBirth and Email fields listed here are required
        #  not required should be entered as null if not available.
        headers = { 'Authorization': f'Bearer {AUTHKEY}', 
        'Content-Type': 'application/json' }

        appDict = {
        "firstName":UserQuery.firstname,
        "middleName":None,
        "lastName":UserQuery.lastname,
        "dob":VerifyQuery.dob,
        "ssn":VerifyQuery.ssn,
        "email":UserQuery.email,
        "address":ContactInfoQuery.residentialaddress,
        "houseNumber":None,
        "streetName":None,
        "city":ContactInfoQuery.city,
        "state":ContactInfoQuery.state,
        "zipCode":ContactInfoQuery.zipcode
        }
        json_object = json.dumps(appDict) 
        print(headers)
        print(json_object)
        resp = requests.post(url = 'https://api-v3-stage.authenticating.com/user/create', headers=headers, data=json_object)
        print(resp)

        if resp.status_code == 401:
            print(resp)
            statement = resp.json()
            print(statement)

        # <Response [400]> 
        if resp.status_code == 400:
            print(resp)
            statement = resp.json()
            print(statement)
            
        
        if resp.status_code == 200:
            statement = resp.json()
            print(statement)
            
    return 'AccessCode Reterived', statement

def SubmitUserConsent(userAccessCode, production):
    global statement
    production = False

    # MockAPI
    if(production == False):

        appDict = {
        "userAccessCode":userAccessCode,
        "GLBPurposeAndDPPAPurpose":1,
        "FCRAPurpose":1,
        "isBackgroundDisclosureAccepted":1,
        "fullName":"Jonathan Doe"
            }

        headers = {
        'content-type': 'application/json',
        }

        print(headers)
        resp = requests.post(url = 'https://api-v3-stage.authenticating.com/mock/user/consent', headers=headers, json=appDict)
        print(resp)

        if resp.status_code == 401:
            print(resp)
            statement = resp.json()
            print(statement)

        # <Response [400]> 
        if resp.status_code == 400:
            print(resp)
            statement = resp.json()
            print(statement)

        if resp.status_code == 200:
            statement = resp.json()
            print(statement)

        return 'Successful Consent'

    if(production == True):

        # How to capture user consent?>
        Auth = AuthTable.query.filter_by(AccessCode=userAccessCode).first()
        username = Auth.username
        UserQuery = UserReact.query.filter_by(username=username).first()
        Auth.userAccessCode
        
        FullName = UserQuery.firstname + UserQuery.lastname
        
        headers = { 'Authorization': f'Bearer {AUTHKEY}', 
            'Content-Type': 'application/json' }

        appDict = {
        "userAccessCode":Auth.userAccessCode,
        "GLBPurposeAndDPPAPurpose":1,
        "FCRAPurpose":1,
        "isBackgroundDisclosureAccepted":1,
        "fullName":FullName
            }

        print(headers)
        resp = requests.post(
            url = 'https://api-v3-stage.authenticating.com/mock/user/consent', 
            headers=headers, json=appDict)
        print(resp)


        if resp.status_code == 401:
            print(resp)
            statement = resp.json()
            print(statement)

        # <Response [400]> 
        if resp.status_code == 400:
            print(resp)
            statement = resp.json()
            print(statement)
            
        if resp.status_code == 200:
            statement = resp.json()
            print(statement)

        return 'Successful Consent'

# We create user 

def VerifyPhone(username):
    # Production Only
    # query AccessCode
    Auth = AuthTable.query.filter_by(username=username).first()
    # 
    data = np.random.randint(100,size=(12))
    
    headers = { 'Authorization': f'Bearer {AUTHKEY}', 
            'Content-Type': 'application/json' }
    #   -H 'cache-control: no-cache' \
    appDict = {
        "userAccessCode":Auth.userAccessCode,
        }

    # 
    resp = requests.post(
            url = 'https://api-v3.authenticating.com/user/verifyPhone', 
            headers=headers, json=appDict)

    return 'pass'

def SMSPhoneCode(username):
    # Production Only
    # VerifyPhoneCode
    # query AccessCode
    Auth = AuthTable.query.filter_by(username=username).first()
    # 
    data = np.random.randint(100,size=(12))
    
    headers = { 'Authorization': f'Bearer {AUTHKEY}', 
            'Content-Type': 'application/json' }

    appDict = {
        "userAccessCode":Auth.userAccessCode,
        "code":data
        }

    # 
    resp = requests.post(
            url = 'https://api-v3.authenticating.com/user/verifyPhoneCode', 
            headers=headers, json=appDict)

    return 'pass'


def VerifyEmail(username):
    Auth = AuthTable.query.filter_by(username=username).first()
        
    headers = { 'Authorization': f'Bearer {AUTHKEY}', 
            'Content-Type': 'application/json' }
    #  -H 'cache-control: no-cache' \
    appDict = {
        "userAccessCode":Auth.userAccessCode,
        }

    # 
    resp = requests.post(
            url = 'https://api-v3.authenticating.com/user/verifyEmail', 
            headers=headers, json=appDict)

    # we expect a true or false back
    return 'pass'

## we call create user endpoint 

# So basically we can only verify after 
# First Name Last Name DateOfBirth and email is requires 

def UploadID(username):

    # OCR scan 
    # compared to and corrected with data extracted from barcode
    # AAMVA standards?

    Auth = AuthTable.query.filter_by(username=username).first()
        
    headers = { 'Authorization': f'Bearer {AUTHKEY}', 
            'Content-Type': 'application/json' }
    #  -H 'cache-control: no-cache' \
    # we need user upload functionality only
    # pnly JPEG or PNG
    appDict = {
        "userAccessCode":Auth.userAccessCode,
        "idFront": "BASE_64_ENCODED_ID_FRONT",
        "idBack": "BASE_64_ENCODED_ID_BACK",
        "country": "COUNTRY_CODE"
        }

    # 
    resp = requests.post(
            url = 'https://api-v3.authenticating.com/identity/document/scan', 
            headers=headers, json=appDict)

    return 'pass'

## Boolean is triggered after a check is done on the database to see if
## a user has sumbitted all the required data, verification has to be done 
# in a 24 hour to 48 period 
# This is either celery gevent solution or asyncio solution and APSscheduler solution
# https://stackoverflow.com/questions/21214270/how-to-schedule-a-function-to-run-every-hour-on-flask
# https://blog.gevent.org/
# https://docs.python.org/3.4/library/asyncio.html
# https://pypi.org/project/APScheduler/


## so we call query ReactUser, ContactInfo, Verify
## for information of FirstName,LastName, DOB  to return AccessCode
## 




## We make another datatable with user_id, First Name + LastName  for easy query and date_uploaded
## we wait for access code to be used for every call and given to (user)

# curl --location --request POST 'https://api-v3-stage.authenticating.com/mock/user/consent' \
# --header 'Content-Type: application/json' \
# --data-raw '{
#     "userAccessCode":"USER_ACCESS_CODE",
#     "GLBPurposeAndDPPAPurpose":1,
#     "FCRAPurpose":1,
#     "isBackgroundDisclosureAccepted":1,
#     "fullName":"Jonathan Doe"
# }'

# we need update functionality 

# To provide "UserConset" we have to match the name in the User Object to this name in the API 

# We can only do this after SSN verification, phone number verification
# So we need to wait for Upload ID or Upload Passport 
# to check the status on the upload id endpoint, you can make a call to Check Upload ID or Check Upload Passport 
# https://docs.authenticating.com/#upload-id
# https://docs.authenticating.com/#upload-passport


# if it requires retry or not 

if __name__ == "__main__":
    username = 'test'
    mockAPI = True
    msg, value = CreateAccessCode(username, mockAPI)
    print(value)
    SubmitUserConsent(value["userAccessCode"], mockAPI)