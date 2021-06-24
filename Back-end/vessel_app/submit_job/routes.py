
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

# @bp.route('/job_drill', methods=['POST'])
# def job():
#     if request.method == 'POST':
#         session_id = request.form.get('session_id')
#         model_name = request.form.get('model_name')
        
#         print(f'Job Submit Page ({model_name})')
#         # get form from selected model
#         from vessel_app.Drill import ml_models
#         drivers = get_ml_drivers(ml_models) # from utils
#         for driver in drivers:
#             if driver.create_drill().name == model_name:
#                 form = driver.create_form()
                

#         return render_template('job_submit.html', form = form, model_name=model_name, session_id=session_id)
#     else:
#         return 'BAD METHOD', 500
    