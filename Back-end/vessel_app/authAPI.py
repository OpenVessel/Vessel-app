
import os
from os import environ, path
from dotenv import load_dotenv
import json
import requests

# basedir = os.path.abspath(os.path.dirname(__file__))
basedir = r'D:\L_pipe\vessel_app_celery\Vessel-app\Back-end'
pathtoenv = path.join(basedir,'.flaskenv')
print(pathtoenv)
load_dotenv(pathtoenv)

## Call company API key from Authenticating SDK 
AUTHKEY = os.environ.get("AUTH_COMPANY_ADMIN_KEY_GOES_HERE")
print(AUTHKEY)


def CreateAcessCode(mockAPI):

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

    # Produciton
    if mockAPI == False:
            # Fake data 
        appDict = {
        "firstName":"Patrick",
        "middleName":"",
        "lastName":"Lastnameson",
        "dob":"29-05-1980",
        "ssn":"123456789",
        "email":"email@email.com",
        "address":"House Number 3, Street Name",
        "houseNumber":"123",
        "streetName":"Hollywood Boulevard",
        "city":"Los Angeles",
        "state":"LA",
        "zipCode":"90210"
        }
    # app_json = json.dumps(appDict)

        headers = { 'Authorization': f'Bearer {AUTHKEY}', 
        'Content-Type': 'application/json' }
        print(headers)
        resp = requests.post(url = 'https://api-v3-stage.authenticating.com/mock/user/create', headers=headers, data=appDict)
        print(resp)

        if resp.status_code == 200:
            statement = resp.json()
            print(statement)

    #new data JSON request 
    ## sent new request with API key
    ##

    return 'AccessCode Reterived'

# We create user 

## we call create user endpoint 
# Please note that this is not included within the Android and IOS SDKs.

# So basically we can only verify after 
# First Name Last Name DateOfBirth and email is requires 



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
    mockAPI = True
    CreateAcessCode(mockAPI)