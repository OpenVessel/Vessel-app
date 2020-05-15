
import sys
import os 
import numpy as np
import scipy
import pydicom 

# from concurrent.futures import ProcessPoolExecutor # Imports multithreading

#https://github.com/lfz/DSB2017

# vessel functions 
from vessel_fun import load_scan, get_pixels_hu, resample, sample_stack
from mask_fun import make_lungmask, plot_3d

### Job queues from the Job engine


## 
## GLOBAL VAR
Threshold = 30 



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


### LOAD SCAN works fine

#pydicom 
patient = load_scan(test_data_pathway)  


## need function generate dictioanry of metadata 
print("Patient number: 1" )
print ("Slice Thickness: %f" % patient[0].SliceThickness)
print ("Pixel Spacing (row, col): (%f, %f) " % (patient[0].PixelSpacing[0], patient[0].PixelSpacing[1]))

#ead all slices are read
image_stack = get_pixels_hu(patient)

print(image_stack)

#np.save(output_numpy + "\\" +  "fullimage_stack" + ".npy", image_stack)
#np.save(output_numpy + "fullimages_" + test_data_pathway + ".npy" , image_stack)

 
## LOAD DATA FROM NUMPY DATA LAKE
## Mask Application and displaying 
Patient_numpy_data = output_numpy
Pat_num_list = os.listdir(Patient_numpy_data)
print(Pat_num_list)

masked_lung = []
imgs_to_process = np.load(Patient_numpy_data + "/"+ Pat_num_list[0])


## Resampling
print ("Shape before resampling\t", imgs_to_process.shape)
imgs_after_resamp, spacing = resample(imgs_to_process, patient, [1,1,1]) #resampling: decreases length and width of dicom file , to normalize data
print ("Shape after resampling\t", imgs_after_resamp.shape)
  


for img in imgs_after_resamp: #loops through images and applies mask
  masked_lung.append(make_lungmask(img))

#sample_stack(masked_lung)
  #np.save(mask_output + "maskedimages_" + pat_files_path[i] + ".npy", masked_lung)

mask = np.array(masked_lung)

#print("Printing Object details")
#print("Shape of Mask", mask.Shape)

## 3D displayer edit function
          #thresholding 

plot_3d(mask, -300)
#https://pybind11.readthedocs.io/en/stable/intro.html
#print("Completed") 

#import SimpleITK as sitk
#volume = sitk.ReadImage('l3d/heat.mhd')
#volume = sitk.GetArrayFromImage(volume)

#import k3d
#plot = k3d.plot()
#isosurface = k3d.marching_cubes(volume, level=1, color=0x801818)
#plot += isosurfaceplot.display 

# with ProcessPoolExecutor() as executor: # This allows multithreading
  
