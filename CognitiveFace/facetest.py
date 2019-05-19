from __future__ import print_function
import numpy as np
import cv2
from matplotlib.pyplot import imshow
from matplotlib.pyplot import rcParams
from matplotlib.patches import Polygon
from matplotlib.pyplot import gcf, gca
import requests
import PIL
import base64
import io
import time

### CAPTURE VIDEO
cam = cv2.VideoCapture(0)
ret, img = cam.read()
cv2.destroyAllWindows() 
cam.release()

rcParams['figure.figsize'] = (12, 8)

#imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))



img_filename = 'opencv_frame_0.png'
data = open(img_filename, "rb").read()



endpoint = 'https://westcentralus.api.cognitive.microsoft.com/face/v1.0/detect'
args = {'returnFaceId': 'true',
        'returnFaceLandmarks': 'false',
        'returnFaceAttributes': 'age,gender,emotion'}
headers = {'Content-Type': 'application/octet-stream',
           'Ocp-Apim-Subscription-Key': 'ec6542b892234b82b987f6f00a359abf'}

response = requests.post(data=data,url=endpoint,headers=headers,params=args)
# r = requests.post(endpoint,
#                   params=args,
#                   headers=headers,
#                   data=img_data)
print(response.json())




ax = imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
for face in response.json():
    print("here")
    rect = face['faceRectangle']
    fattr = face['faceAttributes']
    left, top, width, height = rect['left'], rect['top'], rect['width'], rect['height']
    path = [[left, top], [left + width, top], 
            [left + width, top + height], [left, top + height]]
    ax.axes.add_patch(Polygon(path, edgecolor='red', facecolor='none'))
    disp = {'gender': fattr['gender'],
                 'age': fattr['age']}
    disp.update(fattr['emotion'])
    print(disp)
    for i, k in enumerate(disp):
        ax.axes.text(left+width+5, top + 16 + 40*i, "{0}: {1}".format(k, disp[k]),
                     color='lime', fontsize=16, backgroundcolor='black')

time.sleep(100)