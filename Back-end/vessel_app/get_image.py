import base64
from base64 import b64encode

def extract_image(raw_image):
    image_64= base64.b64encode(raw_image)
    print(type(image_64))
    imgdata = base64.b64decode(image_64)
    filename = 'D:\\Openvessel\\vessel-app\\Back-end\\vessel_app\\static\\media\\some_image.png' 
    print(filename)

    with open(filename, 'wb') as f:
        f.write(imgdata)
    
    return filename