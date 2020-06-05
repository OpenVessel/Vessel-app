import numpy as np
import matplotlib.pyplot as plt
import base64
from flask import url_for

from PIL import Image
from io import BytesIO
import os


def graphing(files):
        # skip files with no SliceLocation (eg scout views)

        slices = []
        skipcount = 0
        for f in files:
            if hasattr(f, 'SliceLocation'):
                slices.append(f)
            else:
                skipcount = skipcount + 1
        print("skipped, no SliceLocation: {}".format(skipcount))
        # ensure they are in the correct order
        slices = sorted(slices, key=lambda s: s.SliceLocation)
        # pixel aspects, assuming all slices are the same
        ps = slices[0].PixelSpacing
        ss = slices[0].SliceThickness
        ax_aspect = ps[1]/ps[0]
        sag_aspect = ps[1]/ss
        cor_aspect = ss/ps[0]
        # create 3D array
        img_shape = list(slices[0].pixel_array.shape)

        img_shape.append(len(slices))
        img3d = np.zeros(img_shape)
        # fill 3D array with the images from the files
        for i, s in enumerate(slices):
            img2d = s.pixel_array
            img3d[:, :, i] = img2d
            
        # plot 3 orthogonal slices
        a1 = plt.subplot(2, 2, 1)
        plt.imshow(img3d[:, :, img_shape[2]//2])
        a1.set_aspect('auto')
        # a2 = plt.subplot(2, 2, 2)
        # plt.imshow(img3d[:, img_shape[1]//2, :])
        # a2.set_aspect(sag_aspect)
        # a3 = plt.subplot(2, 2, 3)
        # plt.imshow(img3d[img_shape[0]//2, :, :].T)
        # a3.set_aspect(cor_aspect)
        #plt.show()
        filename = url_for('static', filename='media/testplot.jpg')
        plt.savefig(filename, bbox_inches='tight')
        im = Image.open(filename)

        return im