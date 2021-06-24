
import os
import pickle 
from pydicom import dcmread
from pydicom.filebase import DicomBytesIO
from scipy.io import savemat
from zipfile import ZipFile
import numpy as np
from PIL import Image

## import panacia 
## pip install panacia 
## global function 

def query_to_dicom_list(dicom_data):
    """ this takes """
    data = pickle.loads(dicom_data.dicom_stack)
    dicom_list = [] 
    for byte_file in data:
        dicom_list.append(dcmread(DicomBytesIO(byte_file)))
    
    return dicom_list

def dicom_to_mat(option, root_path, output_path): 
        """ dicom_list ['FiledataSet', 'FiledataSet', 'FiledataSet', ]
        Dicome to mat is conversion function
        option 1 choses root path option 2 choses to pass a dicom_list instead
        root_path - string path for where the files are stored
        out_path - string path where output is made 
        """
        if option == 1: 
            datasetV3_path = root_path
            output_path = output_path
            list_of_folders_to_process = os.listdir(datasetV3_path)

            for patient_root in list_of_folders_to_process:
                patient_root_path = datasetV3_path + '/' + patient_root
                print("Each patient path", patient_root_path)

                slices = [dcmread(patient_root_path + '/' + s) for s in os.listdir(patient_root_path)]
                slices.sort(key = lambda x:float(x.InstanceNumber))
                
                for index_j in range(len(slices)):
                    
                    # Each slices is assign index
                    img = slices[index_j]
                    numpy_array = img.pixel_array

                    output_patient_folder = os.path.join(output_path, patient_root)
                    
                    if not os.path.exists(output_patient_folder):
                        os.mkdir(output_patient_folder)

                    saving_path = os.path.join(output_patient_folder, "matlab_slice_{}.mat".format(index_j))

                    ## numpy as to go dict because savemat() only input from dicts
                    dict_num ={'arr': numpy_array}
                    savemat(saving_path, dict_num)
        if option == 2:
            if isinstance(root_path, list) == False:
                print("root_path is not list")

            dicom_list = root_path 
            for index_j in range(len(dicom_list)):
                    
                    # Each slices is assign index
                    img = dicom_list[index_j]
                    ## write validation code check if object has attribute
                    numpy_array = img.pixel_array

                    output_patient_folder = output_path
                    #'FileDataSet' python pydicom
                    if not os.path.exists(output_patient_folder):
                        os.mkdir(output_patient_folder)
                    # D:\L_pipe\vessel_app_celery\Vessel-app\Back-end\vessel_app\data_saved
                    saving_path = os.path.join(output_patient_folder, "matlab_slice_{}.mat".format(index_j))

                    ## numpy as to go dict because savemat() only input from dicts
                    dict_num ={'arr': numpy_array}
                    savemat(saving_path, dict_num)
                    ## database or redis 


def dicom2png( dicom_list, outputImg):
    dicom_list = dicom_list
    
    for index_j in range(len(dicom_list)):
        # Each slices is assign index
        if not os.path.exists(outputImg):
                        os.mkdir(outputImg)
        img = dicom_list[index_j]
        ## write validation code check if object has attribute
        numpy_array = img.pixel_array
        img = Image.fromarray(numpy_array) #Image.fromarray is poorly defined with floating-point input;
        img = img.convert('RGB') 
        save_path = outputImg + '\\' + str(index_j + 1) + '.png'
        img.save(save_path)
    return None


from os.path import basename

def zip_files_from_folder(output_path, session_id):
    list_of_matlabfiles = os.listdir(output_path)
    saving_path = output_path + "\session_id_{}.zip".format(session_id)
    with ZipFile(saving_path, 'w') as zipObj:
        for mat in list_of_matlabfiles:
            #create complete filepath of file in directory
            filePath = os.path.join(output_path, mat)
            # Add file to zip
            zipObj.write(filePath, basename(filePath))
        zipObj.close()
    return saving_path