import cv2 as cv
import numpy as np

img = cv.imread('cv-lecture1/resources/data.jpg')
if img is None:
    print("❌ Error: Image not found or path is incorrect.")
    exit()
img= cv.resize(img, (600, 300))
hor_img = np.hstack((img,img))
ver_img = np.vstack((img,img))

cv.imshow('Horizontal Stacking', hor_img)
# cv.imshow('Vertical Stacking', ver_img)
cv.waitKey(0)
cv.destroyAllWindows()

