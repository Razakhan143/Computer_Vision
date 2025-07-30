import cv2 as cv
import numpy as np
from objectDetection import detectAndDisplay

img = cv.imread(0)
# img= cv.imread('cv-lecture1/resources/data.jpg')
if img is None:
    print('--(!) No image data -- Break!')
else:
    
    detectAndDisplay(img,eyes_=True,vid=True)

cv.waitKey(0)
cv.destroyAllWindows()