import numpy as np
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import base64

from flask import url_for
from PIL import Image
from io import BytesIO
def graphing(file):
        
        # pixel aspects
        ps = file.PixelSpacing
        ss = file.SliceThickness
        ax_aspect = ps[1]/ps[0]
        sag_aspect = ps[1]/ss
        cor_aspect = ss/ps[0]
        # create 3D array
        img_shape = list(file.pixel_array.shape)
        img_shape.append(1)
        img3d = np.zeros(img_shape)
        # fill 3D array with the images from the files
        img2d = file.pixel_array
        img3d[:, :, 0] = img2d
        # plot orthogonal slice
        ax = plt.subplot(1, 1, 1)
        plt.imshow(img3d[:, :, img_shape[2]//2])
        ax.set_aspect('auto')
        plt.axis('off')
        #save D:\Openvessel\vessel-app\Back-end\vessel_app\static\media\testplot.jpg
        strpath = os.getcwd()
        strFile = strpath + r"\vessel_app\static\media\testplot.jpg"
        if os.path.isfile(strFile):
                os.remove(strFile)   # Opt.: os.system("rm "+strFile)
        plt.savefig(strFile)
        im = Image.open(strFile)
        return im

