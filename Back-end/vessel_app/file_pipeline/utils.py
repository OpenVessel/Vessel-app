# utils.py
import uuid
import logging
import flask
from flask import url_for
import numpy as np
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import base64
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
        strpath = os.getcwd()
        strFile = strpath + r"\vessel_app\static\temp\testplot.jpg"
        if os.path.isfile(strFile):
                os.remove(strFile)   # Opt.: os.system("rm "+strFile)
        plt.savefig(strFile)
        im = Image.open(strFile)
        return im

# Generate a new request ID, optionally including an original request ID
def generate_request_id(original_id=''):
    new_id = uuid.uuid4()

    if original_id:
        new_id = "{},{}".format(original_id, new_id)

    return new_id

# Returns the current request ID or a new one if there is none
# In order of preference:
#   * If we've already created a request ID and stored it in the flask.g context local, use that
#   * If a client has passed in the X-Request-Id header, create a new ID with that prepended
#   * Otherwise, generate a request ID and store it in flask.g.request_id
def request_id():
    if getattr(flask.g, 'request_id', None):
        return flask.g.request_id

    headers = flask.request.headers
    original_request_id = headers.get("X-Request-Id")
    new_uuid = generate_request_id(original_request_id)
    flask.g.request_id = new_uuid

    return new_uuid

class RequestIdFilter(logging.Filter):
    # This is a logging filter that makes the request ID available for use in
    # the logging format. Note that we're checking if we're in a request
    # context, as we may want to log things before Flask is fully loaded.
    def filter(self, record):
        record.request_id = request_id() if flask.has_request_context() else ''
        return True

def dicom_to_thumbnail(dicom_object):
    tn = graphing(dicom_object)
    size = (300, 300)
    tn.thumbnail(size)
    # convert thumbnail to bytes
    def imgToBytes(img):
        img_bytes = BytesIO()
        img.save(img_bytes, format='PNG')
        img_bytes = img_bytes.getvalue()
        return img_bytes
    tn_bytes = imgToBytes(tn)

    return tn_bytes