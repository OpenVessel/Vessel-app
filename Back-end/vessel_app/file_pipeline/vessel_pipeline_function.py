import os
import pydicom 
import numpy as np
import skimage
import scipy.ndimage

## displayer
import sys
try:    
    import pyvista as pv
except:
    print('import pyvista failed')

from scipy import misc
from pydicom import dcmread
import matplotlib.pyplot as plt
from io import BytesIO
import pickle 
import tempfile
try:
    import vtk
except:
    print('import vtk failed')

import sklearn
import scipy
from skimage import morphology, measure
from skimage.transform import resize
from sklearn.cluster import KMeans
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

import matplotlib.pyplot as plt
from concurrent.futures import ProcessPoolExecutor

try:
    import plotly
    from plotly import __version__
    from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
    from plotly.tools import FigureFactory as FF
    from plotly.graph_objs import *
    import plotly.graph_objects as go
except:
    print('import plotly failed')

## loads the whole folder
def load_scan(slices):
    ## all slices are put into the array
    slices.sort(key = lambda x: int(x.InstanceNumber))
    ##
    try:
        slice_thickness = np.abs(slices[0].ImagePositionPatient[2] - slices[1].ImagePositionPatient[2])
    except:
        slice_thickness = np.abs(slices[0].SliceLocation - slices[1].SliceLocation)
        
    for s in slices:
        s.SliceThickness = slice_thickness
        
    return slices

def get_pixels_hu(slices):
    image = np.stack([s.pixel_array for s in slices])
    # Convert to int16 (from sometimes int16), 
    # should be possible as values should always be low enough (<32k)
    image = image.astype(np.int16)

    # Set outside-of-scan pixels to 0
    # The intercept is usually -1024, so air is approximately 0
    # image[image == -2000] = 0
    outside_image = image.min()
    image[image == outside_image] = 0
    
    # Convert to Hounsfield units (HU)
    for slice_number in range(len(slices)):
        
        intercept = slices[slice_number].RescaleIntercept
        slope = slices[slice_number].RescaleSlope
        
        if slope != 1:
            image[slice_number] = slope * image[slice_number].astype(np.float64)
            image[slice_number] = image[slice_number].astype(np.int16)
            
        image[slice_number] += np.int16(intercept)
    
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

def displayer(numpy_mask):
    data_matrix = numpy_mask
    opacity = [0, 0, 0, 4, 8, 0, 0] 
    data = pv.wrap(data_matrix)

    pv.set_plot_theme("night")
    #print(type(data)) #pyvista.core.grid.UniformGrid'
    #print(dir(data)) #x = pickle.dumps(data) #print(x)
    #print(BytesIO(data))
    return data

def temp_file_db():
    with tempfile.NamedTemporaryFile(delete=False,suffix=".vti") as tf: 
        if not tf.name:
            print("tempfile name does not exist")
        else:
            print("tempfile made -- temp_file_db")
        
    return tf.name

def pickle_vtk(mesh):
    writer = vtk.vtkDataSetWriter() # create instance of writer
    writer.SetInputDataObject(mesh) # input the data as a vtk object
    writer.SetWriteToOutputString(True) # instead of writing to file
    writer.SetFileTypeToASCII()
    writer.Write()
    to_serialize = writer.GetOutputString()

    output = pickle.dumps(to_serialize, protocol=pickle.HIGHEST_PROTOCOL)

    return output

def unpickle_vtk(data):
    unpickled_data = pickle.loads(data) # data is a result of writer.GetOutputString()
    reader = vtk.vtkDataSetReader()

    # Which one to use?
    # reader.SetReadFromInputString(True)
    reader.ReadFromInputStringOn()
    reader.SetInputString(unpickled_data)
    # reader.ReadAllVectorsOn()
    # reader.ReadAllScalarsOn()
    reader.Update()
    data = pv.wrap(reader.GetOutput())

    return data # this is a vtk object being returned

def unpickle_vtk_2(filename):
    with open(filename, 'rb') as handle:
        to_deserialize = pickle.load(handle)

    reader = vtk.vtkDataSetReader()
    reader.ReadFromInputStringOn()
    reader.SetInputString(to_deserialize)
    reader.Update()
    return pv.wrap(reader.GetOutput())



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
## LUNG MASK LUNG SEGMENTATION
## 3D display
## Standardize the pixel values
## skimage algorithms for image processing

def make_lungmask(img, n_clusters=2, display=False):
    row_size= img.shape[0]
    col_size = img.shape[1]
    
    mean = np.mean(img)
    std = np.std(img)
    img = img-mean
    img = img/std
    # Find the average pixel value near the lungs
    # to renormalize washed out images
    middle = img[int(col_size/5):int(col_size/5*4),int(row_size/5):int(row_size/5*4)] 
    mean = np.mean(middle)  
    max = np.max(img)
    min = np.min(img)
    # To improve threshold finding, I'm moving the 
    # underflow and overflow on the pixel spectrum
    img[img==max] = mean
    img[img==min] = mean
    #
    # Using Kmeans to separate foreground (soft tissue / bone) and background (lung/air)
    #sensitive to outliers and noise Kmeans could be really bad 
    # https://www.youtube.com/watch?v=_aWzGGNrcic

    kmeans = KMeans(n_clusters=n_clusters).fit(np.reshape(middle,[np.prod(middle.shape),1]))
    centers = sorted(kmeans.cluster_centers_.flatten())
    ###
    threshold = np.mean(centers)
    thresh_img = np.where(img<threshold,1.0,0.0)  # threshold the image

    # First erode away the finer elements, then dilate to include some of the pixels surrounding the lung.  
    # We don't want to accidentally clip the lung.

    eroded = morphology.erosion(thresh_img,np.ones([3,3]))
    dilation = morphology.dilation(eroded,np.ones([8,8]))

    labels = measure.label(dilation) # Different labels are displayed in different colors
    label_vals = np.unique(labels)
    regions = measure.regionprops(labels)
    good_labels = []
    for prop in regions:
        B = prop.bbox
        if B[2]-B[0]<row_size/10*9 and B[3]-B[1]<col_size/10*9 and B[0]>row_size/5 and B[2]<col_size/5*4:
            good_labels.append(prop.label)
    mask = np.ndarray([row_size,col_size],dtype=np.int8)
    mask[:] = 0

    #
    #  After just the lungs are left, we do another large dilation
    #  in order to fill in and out the lung mask 
    #
    for N in good_labels:
        mask = mask + np.where(labels==N,1,0)
    mask = morphology.dilation(mask,np.ones([10,10])) # one last dilation

    if (display):
        fig, ax = plt.subplots(3, 2, figsize=[12, 12])
        ax[0, 0].set_title("Original")
        ax[0, 0].imshow(img, cmap='gray')
        ax[0, 0].axis('off')
        ax[0, 1].set_title("Threshold")
        ax[0, 1].imshow(thresh_img, cmap='gray')
        ax[0, 1].axis('off')
        ax[1, 0].set_title("After Erosion and Dilation")
        ax[1, 0].imshow(dilation, cmap='gray')
        ax[1, 0].axis('off')
        ax[1, 1].set_title("Color Labels")
        ax[1, 1].imshow(labels)
        ax[1, 1].axis('off')
        ax[2, 0].set_title("Final Mask")
        ax[2, 0].imshow(mask, cmap='gray')
        ax[2, 0].axis('off')
        ax[2, 1].set_title("Apply Mask on Original")
        ax[2, 1].imshow(mask*img, cmap='gray')
        ax[2, 1].axis('off')
        
        plt.show()
    return mask*img


def make_lungmask_v2(img, n_clusters,  display = False):
    row_size= img.shape[0]
    col_size = img.shape[1]
    mean = np.mean(img)
    std = np.std(img) 
    img = (img-mean)/std # Subtracts mean and divide standard deviation from each element ## Standardises the whole data

    # Find the average pixel value near the lungs
    # to renormalize washed out images
    # middle = img
    middle = img[int(col_size/5):int(col_size/5*4),int(row_size/5):int(row_size/5*4)]
    # print(middle.shape)
    
    mean = np.mean(middle)  
    max = np.max(img)
    min = np.min(img)
    
    # To improve threshold finding, I'm moving the 
    # underflow and overflow on the pixel spectrum
    img[img==max]=mean # Goes through the list and if anything equals max, it changes its value to mean.
    img[img==min]=mean # Goes through the list and if anything equals min, it changes its value to mean.

    # Using Kmeans to separate foreground (soft tissue / bone) and background (lung/air)
    #sensitive to outliers and noise Kmeans could be really bad 
    # https://www.youtube.com/watch?v=_aWzGGNrcic
    kmeans = KMeans(n_clusters=n_clusters).fit(np.reshape(middle,[np.prod(middle.shape),1]))
    centers = sorted(kmeans.cluster_centers_.flatten())
    
    threshold = np.mean(centers)
    # thresh_img = np.where(img<threshold,1.0,0.0)  # threshold the image
    thresh_img = np.where(img<threshold, 3.0,0.0)

    # First erode away the finer elements, then dilate to include some of the pixels surrounding the lung.  
    # We don't want to accidentally clip the lung.

    eroded = morphology.erosion(thresh_img,np.ones([3,3]))
    dilation = morphology.dilation(eroded,np.ones([8,8]))

    ## START here
    labels = measure.label(dilation) 
    # Different labels are displayed in different colors

    label_vals = np.unique(labels)
    ## ok region props what is this 
    regions = measure.regionprops(labels)
    good_labels = []
    
    # what is this SECTION OF CODE?? 
    # why is it ommitting half the lung 
    # This choses the output.
    for prop in regions:
        B = prop.bbox

        if B[2]-B[0]<row_size/10*9 and B[3]-B[1]<col_size/10*9 and B[0]>row_size/5 and B[2]<col_size/3*4:
            good_labels.append(prop.label)

    mask = np.ndarray([row_size,col_size],dtype=np.int8)
    mask[:] = 0

    #  After just the lungs are left, we do another large dilation
    #  in order to fill in and out the lung mask 
    for N in good_labels:
        mask = mask + np.where(labels==N,1,0)
        # print("N:", N)
    mask = morphology.dilation(mask,np.ones([10,10])) # one last dilation

    if display:
        fig, (ax1, ax2, ax3) = plt.subplots(1, 3, sharey = 'row', figsize=[18, 8])
        ax1.set_title("Original Slice")
        ax1.imshow(img, cmap='gray')
        ax1.axis('off')

        ax2.set_title("Color Labels")
        ax2.imshow(labels)
        ax2.axis('off')
        
        ax3.set_title("First Mask on Original")
        ax3.imshow(mask*img, cmap='gray')
        ax3.axis('off')

        plt.show()

    return mask*img


def largest_label_volume(im, bg=-1):
    vals, counts = np.unique(im, return_counts=True)

    counts = counts[vals != bg]
    vals = vals[vals != bg]

    if len(counts) > 0:
        return vals[np.argmax(counts)]
    else:
        return None
