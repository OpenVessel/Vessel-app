import uuid
import logging
import flask

def temp_session_id(current_app, current_user):
    session = {'id':'no_id'}
    internal_endpoints = [rule.endpoint for rule in current_app.url_map.iter_rules()]
    try:
        # print("Output before -------- ",session['last_endpoint'])
        pass
    except:
        session['last_endpoint'] = 'nowhere'
        # print("Output before -------- ",session['last_endpoint'])
    
    if current_user.is_authenticated == False:

        # create session_id
        session['id'] = request_id()
        return session


# Generate a new request ID, optionally including an original request ID
def generate_request_id(original_id=''):
    new_id = uuid.uuid4()

    if original_id:
        new_id = "{},{}".format(original_id, new_id)

    return new_id

# Returns the current request ID or a new one if there is none
# In order of preference:
#   * If we've already created a request ID and stored it in the flask.g context local, use that
#   * If a client has passed in the X-Request-Id header, create a new ID with that prepended
#   * Otherwise, generate a request ID and store it in flask.g.request_id
def request_id():
    if getattr(flask.g, 'request_id', None):
        return flask.g.request_id

    headers = flask.request.headers
    original_request_id = headers.get("X-Request-Id")
    new_uuid = generate_request_id(original_request_id)
    flask.g.request_id = new_uuid

    return new_uuid