import os
import pydicom
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import tempfile
import base64
import shutil
import pickle
import time
import logging
from datetime import datetime as dt
from PIL import Image
from io import BytesIO
from pydicom import dcmread
from pydicom.filebase import DicomBytesIO
from pydicom.charset import encode_string
from pydicom.datadict import dictionary_description as dd
from flask import render_template, url_for, flash, redirect, request, session, after_this_request, current_app, Response
from flask_login import current_user, login_required, login_user
from base64 import b64encode
from vessel_app.models import User, Dicom, DicomFormData, Object_3D, DicomMetaData

from . import bp

@bp.route('/browser_list')
@login_required
def browser_list():

    print('generating browser')
    ###### Query Database and Indexing ######
    dicom_data = Dicom.query.filter_by(user_id=current_user.id).all()

    #FileDataset part pydicoms
    all_studies = []
    images_list_path = []

    ######  DICOM data to dataframes function ######
    print('---- BROWSER DATA ----')
    for file_num, k in enumerate(dicom_data): #k is each row in the query database
        data = pickle.loads(k.dicom_stack)
        raw_image = BytesIO(k.thumbnail).read()
        file_count = k.file_count
        session_id = k.session_id

        print(k.formData)
        print('CARD SESSION ID:', session_id)

        study_name = k.formData.study_name
        description = k.formData.description

        ## session_id_3d
        try:
            session_id_3ds = [(k.date_uploaded, k.session_id_3d) for k in Object_3D.query.filter_by(session_id=session_id).all()]
        except:
            session_id_3ds = []

        all_rows_in_study = [] # [{}, {}, {}]
        cols = [] # list of list of each column for each

        for byte_file in data: # list of all dicom files in binary
            raw = DicomBytesIO(byte_file)
            dicom_dict = []
            for k,v in dcmread(raw).items():
                try:
                    pair = (dd(k),v)
                except KeyError:
                    pair = (str(k), v)
                dicom_dict.append(pair)
            dicom_dict = dict(dicom_dict)
            # dicom_dict = dict([(dd(k),v) for k,v in dcmread(raw).items()])
            all_rows_in_study.append(dicom_dict)
            cols.append(list(dicom_dict.keys()))
        all_encompassing_cols = list(set([x for l in cols for x in l]))     # [[a, b, c], [a, d]] --flatted, set --> [a, b, c, d]
        study_df = pd.DataFrame(all_rows_in_study, columns=all_encompassing_cols)

        # turn bytes of thumbnail into ascii string
        file_thumbnail = base64.b64encode(raw_image).decode('ascii')

        all_studies.append({
            'study_df': study_df,
            'file_thumbnail': file_thumbnail,
            'file_count': file_count,
            'session_id': session_id,
            'session_id_3ds': session_id_3ds,
            'study_name': study_name,
            'description': description
            })

    browserFields = ["Study Date", "Study ID", "Patient ID", "Modality"]
    #print("Print all studies list:",all_studies)
    return render_template('browser_list_view.html',
    all_studies=all_studies,
    browserFields=browserFields)