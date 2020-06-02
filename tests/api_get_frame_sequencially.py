""" Script to test the flask API
"""
from ast import literal_eval
import requests
import numpy as np
import cv2
import matplotlib.pyplot as plt
from PIL import Image

# Base variables and methods
url_base_path = "http://zeus.itleiria.pt:5000/" 


## 1. Select stream
r = requests.get(url_base_path + "select_stream?idx=2")  # post?
print(r.status_code)


## 2. Test Frames
def get_rgb_from_yuv(raw, shape):
    """Convert YUV420 to RGB array!

    :param raw: bytearray received by API
    :type raw: bytearray
    """
    yuv = np.frombuffer(raw, dtype=np.uint8).reshape(shape)
    return cv2.cvtColor(yuv, cv2.COLOR_YUV420P2BGR)  # YV12)

def display_frame_raw(r_content,shape):
    # convert yuv to rgb
    if len(r_content) > 0:
        rgb = get_rgb_from_yuv(r_content, shape)
        # display image
        plt.imshow(rgb)
        plt.show()
    else:
        print("Received an empty bytearray!")

def get_frame(proj):
    """ Auxiliar method to: get_frame_info proj, get_frame_raw proj, display image."""
    # get frame info for ERP
    r_info = requests.get(url_base_path + "get_frame_info?projection="+proj)
    frame_info = literal_eval(r_info.content.decode())
    print("Frame info:", frame_info)

    width = frame_info["width"]
    height = frame_info["height"]
    shape = (int(height * 1.5), width)

    # Get frame raw
    r_content = requests.get(url_base_path + "get_frame_raw?projection="+proj, stream=True).content
    display_frame_raw(r_content,shape)

while( 1 ):
    get_frame("ERP")
