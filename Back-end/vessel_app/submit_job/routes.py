
from flask import render_template, url_for, flash, redirect, request, session, after_this_request, current_app, Response
from . import bp

## lot of drill logic will go here from on 
@bp.route('/job', methods=['POST'])
def job():
    if request.method == 'POST':
        session_id = request.form.get('session_id')
    else:
        return 'BAD METHOD', 500
    return render_template('job_submit.html', session_id=session_id)