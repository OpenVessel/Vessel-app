

#This is an collection of python function for profiling python function 
# # optimizing python functions 
#


## TO DO LIST
    # profile resampling
    #profile Plot_3d and ITK intergration 

import os
import numpy as np

import pstats
import cProfile
import re

from vessel_functions import resample, load_scan

homepath = r"D:\Lung CT"
check = os.getcwd()

list_dir = os.listdir(check)
SPIE_data_path = homepath + r'\SPIE-AAPM Lung CT Challenge'
list_out = os.listdir(SPIE_data_path)

## input
test_data_pathway = r"D:\Lung CT\SPIE-AAPM Lung CT Challenge\CT-Training-BE001\01-03-2007-16904-CT INFUSED CHEST-143.1\4-HIGH RES-47.17"
## need a function check folder and go down until finds DICOM file 
list_dicom_files = os.listdir(test_data_pathway)

## output data stream
output_file = r"D:\Lung CT\output_data"

output_metafile = output_file + r"\metadata"
output_maskfile = output_file + r"\maskdata"
output_numpy = output_file + r"\numpy"


output_numpy = output_file + r"\numpy"

#np.save(output_numpy + "fullimages_" + test_data_pathway + ".npy" , image_stack)

 
## LOAD DATA FROM NUMPY DATA LAKE
## Mask Application and displaying 
Patient_numpy_data = output_numpy
Pat_num_list = os.listdir(Patient_numpy_data)
print(Pat_num_list)

patient = load_scan(test_data_pathway)  

imgs_to_process = np.load(Patient_numpy_data + "/"+ Pat_num_list[0])

def main():
    print("main program")
    print ("Shape before resampling\t", imgs_to_process.shape)
    imgs_after_resamp, spacing = resample(imgs_to_process, patient, [1,1,1]) #resampling: decreases length and width of dicom file , to normalize data
    print ("Shape after resampling\t", imgs_after_resamp.shape)



## What is "if __name__ == ""__main__":??
if __name__ == "__main__":
    cProfile.run("main()", "Profile.prof")
    s = pstats.Stats("Profile.prof")
    s.strip_dirs().sort_stats("time").print_stats(10)

