import cv2 as cv
import numpy as np
# Load the video
img = cv.imread('cv-lecture1\\resources\\data.jpg')

if img is None:
    print("❌ Error: Image not found or path is incorrect.")
else:
    img = img[100:500, 100:300]
    edg_img = cv.Canny(img, 28, 28)
    img = cv.resize(img, (600, 300))
    dialate = np.ones((2, 2), np.uint8)
    edg_img = cv.dilate(edg_img, dialate, iterations=1)
    erod_img = cv.erode(edg_img, dialate, iterations=1)
    # img = cv.GaussianBlur(img, (31, 31), 0)
    # cv.imshow("Blurred", img)
    cv.imshow("erode", erod_img)
    cv.imshow("edge", edg_img)
    cv.waitKey(0)
    cv.destroyAllWindows()