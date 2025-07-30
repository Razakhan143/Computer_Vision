import cv2 as cv

img = cv.imread('resources/dogs.jpg')
img = cv.resize(img, (600, 300))
blur = cv.GaussianBlur(img, (3, 3), 10)

cv.imshow('Blurred Image', blur)
cv.waitKey(0)