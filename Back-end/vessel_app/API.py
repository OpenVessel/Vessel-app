from vessel_app.Drill.job_submit_fields import JobSubmitForm, NumberField, DropdownField
from vessel_app.Drill.drill import Drill
from vessel_app.Drill.ml_models.segmentation import run_model as segmentation

# Populate Job Submit Form

def create_form():

    job_submit_form = JobSubmitForm('Mask Segmentation')

    k_field = NumberField('K Value (1-20):', 'n_clusters', min=1, max=20, placeholder=2, value=2)
    segmentatation_dd = DropdownField('Segmentation Options:', 'segmentation_options', options={'Bone': 350, 'Blood': 55})

    job_submit_form.add_field(k_field)
    job_submit_form.add_field(segmentatation_dd)

    return job_submit_form

def create_drill():
    drill = Drill(segmentation, name='segmentation')

    return drill

