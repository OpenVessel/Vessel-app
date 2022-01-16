import json
import pickle

def JSONtoBLOB():
    # Structure timeline JS takes?
    appDict = {
    'name': 'messenger',
    'playstore': True,
    'company': 'Facebook',
    'price': 100
    }
    app_json = json.dumps(appDict)
    print(app_json)

    binary_blob = pickle.dumps(app_json)

    return binary_blob

def BLOBtoJSON(binary_blob):
    jsonObj = pickle.loads(binary_blob)
    return jsonObj