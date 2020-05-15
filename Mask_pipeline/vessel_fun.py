
##
## FUNCTIONS
##
## this loads the scans
import os
import pydicom 
import numpy as np
import skimage
import scipy.ndimage

from scipy import misc
from pydicom import dcmread
import matplotlib.pyplot as plt

## loads the whole folder
def load_scan(path):
    ## slices = [] is an array
    slices = [dcmread(path + '/' + s) for s in os.listdir(path)]
    ## all slices are put into the array
    ###
    slices.sort(key = lambda x: int(x.InstanceNumber))
    
    ##
    try:
        slice_thickness = np.abs(slices[0].ImagePositionPatient[2] - slices[1].ImagePositionPatient[2])
    except:
        slice_thickness = np.abs(slices[0].SliceLocation - slices[1].SliceLocation)
        
    for s in slices:
        s.SliceThickness = slice_thickness
        
    return slices

def get_pixels_hu(scans):
    image = np.stack([s.pixel_array for s in scans])
    # Convert to int16 (from sometimes int16), 
    # should be possible as values should always be low enough (<32k)
    image = image.astype(np.int16)

    # Set outside-of-scan pixels to 1
    # The intercept is usually -1024, so air is approximately 0
    image[image == -2000] = 0
    
    # Convert to Hounsfield units (HU)
    intercept = scans[0].RescaleIntercept
    slope = scans[0].RescaleSlope
    
    if slope != 1:
        image = slope * image.astype(np.float64)
        image = image.astype(np.int16)
        
    image += np.int16(intercept)
    
    return np.array(image, dtype=np.int16)


## RESAMPLING ALL data
# Image the we resample given  
#Resampling grid
# TTransformation
#Interpolator 

def resample(image, scan, new_spacing=[1,1,1]):

    # Determine current pixel spacing
    # map()? returns a map object passes function to each element of given iterable
    spacing = map(float, ([scan[0].SliceThickness] + list(scan[0].PixelSpacing))) 
    spacing = np.array(list(spacing)) # numpy array

    resize_factor = spacing / new_spacing
    new_real_shape = image.shape * resize_factor
    new_shape = np.round(new_real_shape)
    real_resize_factor = new_shape / image.shape
    new_spacing = spacing / real_resize_factor
    
    #scipy.ndimage.interpolation.zoom
    #The array is zoomed using spline interpolation of the requested order.
    image = scipy.ndimage.interpolation.zoom(image, real_resize_factor)
    
    return image, new_spacing

## show sample stack
def sample_stack(stack, rows=6, cols=6, start_with=15, show_every=4):
    fig,ax = plt.subplots(rows,cols,figsize=[12,12])

    for i in range(rows*cols):
        
        ind = start_with + i*show_every

        if ind < len(stack):
            ax[int(i/rows),int(i % rows)].set_title('slice %d' % ind)
            ax[int(i/rows),int(i % rows)].imshow(stack[ind],cmap='gray')
            ax[int(i/rows),int(i % rows)].axis('off')

    plt.show()


## Histogram functions 
