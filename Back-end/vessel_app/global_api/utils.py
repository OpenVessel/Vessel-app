from flask import jsonify, url_for
import hmac
import os

from hashlib import sha1
from datetime import datetime, timedelta
# https://www.programcreek.com/python/?code=google%2Fgoogleapps-message-recall%2Fgoogleapps-message-recall-master%2Fmessage_recall%2Flib%2Fwtforms%2Fext%2Fcsrf%2Fsession.py
class APIException(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv

def has_no_empty_params(rule):
    defaults = rule.defaults if rule.defaults is not None else ()
    arguments = rule.arguments if rule.arguments is not None else ()
    return len(defaults) >= len(arguments)


TIME_FORMAT = '%Y%m%d%H%M%S'
TIME_LIMIT = timedelta(minutes=30)


def generate_csrf_token(SECRET_KEY,  csrf_context):
    if SECRET_KEY is None:
        raise Exception('must set SECRET_KEY in a subclass of this form for it to work')
    if csrf_context is None:
        raise TypeError('Must provide a session-like object as csrf context')

    session = getattr(csrf_context, 'session', csrf_context)

    if 'csrf' not in session:
        session['csrf'] = sha1(os.urandom(64)).hexdigest()

    csrf_token.csrf_key = session['csrf']
    if TIME_LIMIT:
        expires = (datetime.now() + TIME_LIMIT).strftime(TIME_FORMAT)
        csrf_build = '%s%s' % (session['csrf'], expires)
    else:
        expires = ''
        csrf_build = session['csrf']

    hmac_csrf = hmac.new(SECRET_KEY, csrf_build.encode('utf8'), digestmod=sha1)
    return '%s##%s' % (expires, hmac_csrf.hexdigest())

def generate_sitemap(app):
    links = ['/admin/']
    for rule in app.url_map.iter_rules():
        # Filter out rules we can't navigate to in a browser
        # and rules that require parameters
        if "GET" in rule.methods and has_no_empty_params(rule):
            url = url_for(rule.endpoint, **(rule.defaults or {}))
            if "/admin/" not in url:
                links.append(url)

    links_html = "".join(["<li><a href='" + y + "'>" + y + "</a></li>" for y in links])
    return """
        <div style="text-align: center;">
        <h1>OpenVessel's Global API call for internal use only </h1>
        <p>API HOST: <script>document.write('<input style="padding: 5px; width: 300px" type="text" value="'+window.location.href+'" />');</script></p>
        <p>Start working on your project by following the <a href="https://start.4geeksacademy.com/starters/full-stack" target="_blank">Quick Start</a></p>
        <p>Remember to specify a real endpoint path like: </p>
        <ul style="text-align: left;">"""+links_html+"</ul></div>"


def password_check(passwd):
	
	SpecialSym =['!', '$', '@', '#', '%']
	val = True
	error = ''
	if len(passwd) < 6:
		error = 'length should be at least 6'
		val = False
		
	if len(passwd) > 20:
		error = 'length should be not be greater than 8'
		val = False
		
	if not any(char.isdigit() for char in passwd):
		error = 'Password should have at least one numeral'
		val = False
		
	if not any(char.isupper() for char in passwd):
		error = 'Password should have at least one uppercase letter'
		val = False
		
	if not any(char.islower() for char in passwd):
		error = 'Password should have at least one lowercase letter'
		val = False
		
	if not any(char in SpecialSym for char in passwd):
		error = 'Password should have at least one of the symbols !$@#'
		val = False

	if val:
		return val
