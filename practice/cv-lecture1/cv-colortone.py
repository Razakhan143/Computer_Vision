import cv2 as cv
import numpy as np
# Load the image
img = cv.imread('cv-lecture1/resources/data.jpg')
img = cv.resize(img, (1200, 600))
# Check if image was successfully loaded
gray= cv.cvtColor(img, cv.COLOR_BGR2GRAY)
(thresh , b_w) = cv.thershold(gray,127,255, cv.THRESH_BINARY)

cv.imshow('Original Image', img)
cv.imshow('Gray Scale Image', gray)
cv.imshow('Black and White Image', b_w)

cv.waitKey(0)
cv.destroyAllWindows()
# to save the black and white image
cv.imwrite('resources/b_w_image.jpg', b_w)