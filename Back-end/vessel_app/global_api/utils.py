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

def yearsago(years, from_date=None):
    if from_date is None:
        from_date = datetime.now()
    return from_date + relativedelta(years=years)

# How many days ago
def daysago(today_date, start_date=None):
    if start_date is None:
        return "missing start_date"

    dt = datetime.combine(date.today(), datetime.min.time())

    elapsed_time = dt - start_date
    return elapsed_time

def photo_to_thumbnail(imageObj):
    tn = imageObj
    size = (300, 300)
    tn.thumbnail(size)
    # convert thumbnail to bytes
    def imgToBytes(img):
        img_bytes = BytesIO()
        img.save(img_bytes, format='PNG')
        img_bytes = img_bytes.getvalue()
        return img_bytes
    tn_bytes = imgToBytes(tn)

    return tn_bytes


#### API query for HL7 
## ingestion framewor# machine learning its goes to anothe database or server

##
## After step 25th we are intergrating into existing medical software platforms 
##Epic's APi 
## #https://fhir.epic.com/Documentation?docId=developerguidelines

##
## polygon callsk 
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