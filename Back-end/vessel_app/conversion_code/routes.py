###Default imports or template to start new webpages
from flask import render_template, url_for, flash, redirect, request, session, after_this_request, current_app, send_file
from flask_login import current_user, login_required, login_user
import os
import shutil
from vessel_app import db, bcrypt, dropzone
from vessel_app.models import User, Dicom, DicomFormData, Object_3D
from vessel_app.panaica import query_to_dicom_list, dicom_to_mat, zip_files_from_folder, dicom2png
from . import bp

@bp.route('/convert', methods=['POST'])
def convert():

    if request.method == 'POST':
        file_type = request.form.get('file_types')
        session_id = request.form.get('session_id')

        if file_type == 'matlab':
            output_path = os.getcwd() + "\\vessel_app\data_saved\\matlab_session_id_{}".format(session_id)
            if os.path.exists(output_path):
                shutil.rmtree(output_path)
            dicom_data = Dicom.query.filter_by(session_id=session_id).first()
            dicom_list = query_to_dicom_list(dicom_data)
            
            print(type(dicom_list[1]))
            dicom_to_mat(option=2, root_path=dicom_list, output_path=output_path)
            zip_file_path = zip_files_from_folder(output_path, session_id)
            
            # zip_files_created_memory
            # https://stackoverflow.com/questions/27337013/how-to-send-zip-files-in-the-python-flask-framework
            # https://medium.com/analytics-vidhya/receive-or-return-files-flask-api-8389d42b0684
            
            return send_file(zip_file_path,
            mimetype = 'zip',
            attachment_filename= 'matlab_files.zip',
            as_attachment = True)
            
        if file_type == 'png':
            output_path = os.getcwd() + "\\vessel_app\data_saved\\png_session_id_{}".format(session_id)
            print(output_path)
            if os.path.exists(output_path):
                shutil.rmtree(output_path)
            dicom_data = Dicom.query.filter_by(session_id=session_id).first()
            dicom_list = query_to_dicom_list(dicom_data)
            dicom2png(dicom_list, output_path)
            zip_file_path = zip_files_from_folder(output_path, session_id)
            return send_file(zip_file_path,
            mimetype = 'zip',
            attachment_filename= 'png_files.zip',
            as_attachment = True)

        if file_type == 'jepg':
            pass

        if file_type == 'tiff':
            pass
        
        if file_type == 'jpeg_2000':
            pass

        if file_type == 'jpeg-ls':
            pass

        if file_type == 'RLE':
            pass

        if file_type == 'gif':
            pass


        # formData = DicomFormData(
        #     study_name=study_name,
        #     description=description,
        #     session_id=str(session['id']))
        # db.session.add(formData)
        # db.session.commit()
        # time.sleep(1.5)
        return redirect(url_for('file_pipeline.browser'))


        # data_3ds = Object_3D.query.filter_by(session_id=session_id).all()
        dicom_form_data = DicomFormData.query.filter_by(session_id=session_id).first()
        # dicom and form data
        try:
            db.session.delete(dicom_data)
            db.session.delete(dicom_form_data)
            print(dicom_data, dicom_form_data, 'deleted successfully')
        except:
            print('failed to delete', dicom_data, dicom_form_data)
            return redirect(url_for('errors.internal_error'))
        # 3d data
        if data_3ds != []:
            try:
                for data_3d in data_3ds:
                    db.session.delete(data_3d)
                    print(data_3d, 'deleted successfully')
            except:
                print('failed to delete', dicom_data, dicom_form_data)
                return redirect(url_for('errors.internal_error'))
        db.session.commit()
        print("GOING TO BROWSER")
        return redirect(url_for('file_pipeline.browser'))

    else:
        # this should never get called
        return redirect(url_for('main.index'))