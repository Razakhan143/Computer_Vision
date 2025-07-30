import cv2 as cv
import numpy as np

# Load the image
img = cv.imread('cv-lecture1/resources/data.jpg')
img= cv.resize(img, (1200, 600))
img1 = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
# Check if image was successfully loaded
if img is None:
    print("Error: Image not found or path is incorrect.")
else:
    cv.imshow('Original Image', img)
    cv.imshow('Gray Scale Image', img1)
    cv.waitKey(0)
    cv.destroyAllWindows()
