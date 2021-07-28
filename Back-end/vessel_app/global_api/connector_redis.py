# https://realpython.com/python-redis/

import redis
import uuid
## provides the connection
## we can implement ca-certificattes.crt we need to generate one for flask
redis_server = redis.Redis(host='localhost', port=6379, db=0)

print(redis_server)
# 'redis://localhost:6379/0'
def save_csrf(csrf_token):
    print("hello world")
    try:
        ## we create csrf_token_id = 'csrf_token + uniqe id'
        csrf_token_id = 'csrf_token_'+ str(uuid.uuid4())
        statement = redis_server.set(csrf_token_id , csrf_token)
        print("we saved csrf_token", statement)
        return csrf_token_id
        ## we set asynch function call to delete statement in 45 minutes

    except:
        print("set failed for csrf_token")

    return 

# WERE ARE NOT SURE IF THIS WORKS FOR MUILTPE USERS
def check_csrf_token(token_id, set_boolean=False):
    if set_boolean == False:
        print("we are not checking")
        csrf_token = ""
    else:
        csrf_token = redis_server.get(token_id)
        csrf_token = csrf_token.decode("utf-8") 
        # print(type(csrf_token))

    return csrf_token
## Notes on redis
## key:value pairs 
## keys are strings
## redis data typeps string list hashes sets
