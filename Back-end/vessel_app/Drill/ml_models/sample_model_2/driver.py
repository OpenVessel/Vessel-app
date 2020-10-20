from vessel_app.Drill.job_submit_fields import JobSubmitForm, NumberField, DropdownField
from vessel_app.Drill.drill import Drill
from vessel_app.Drill.ml_models.sample_model_2.model import run_model

# Populate Job Submit Form

def create_form():

    job_submit_form = JobSubmitForm('Sample Model 2')

    num_1 = NumberField('Number Field 1:', 'keyword1', min=1, max=20, placeholder=2, value=2)
    dd_1 = DropdownField('Dropdown Option 1:', 'keyword2', options={'Cheese': 350, 'Ketchup': 55})
    dd_2 = DropdownField('Dropdown Option 2:', 'keyword3', options={'Green': 'green', 'Red': 'red', 'Yellow': 'yellow', 'Orange':'orange'})
    num_2 = NumberField('Number Field 2:', 'keyword4', min=20, max=2000, placeholder=400, value=400)

    job_submit_form.add_field(num_1)
    job_submit_form.add_field(dd_1)
    job_submit_form.add_field(dd_2)
    job_submit_form.add_field(num_2)

    return job_submit_form

def create_drill():
    drill = Drill(run_model, 'Sample Model 2', description='This is a second model that you can choose from.')

    return drill

