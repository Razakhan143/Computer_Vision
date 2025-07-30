import cv2 as cv
import numpy as np

img = cv.imread('cv-lecture1/resources/data.jpg')

hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)

def slider():
    pass
path = 'cv-lecture1/resources/data.jpg'
cv.namedWindow('image')
cv.resizeWindow('image', 400, 200)
cv.createTrackbar('HMin', 'image', 0, 179, slider)
cv.createTrackbar('HMax', 'image', 179, 179, slider)
cv.createTrackbar('SMin', 'image', 0, 255, slider)
cv.createTrackbar('SMax', 'image', 255, 255, slider)
cv.createTrackbar('VMin', 'image', 0, 255, slider)
cv.createTrackbar('VMax', 'image', 255, 255, slider)


img = cv.imread(path)
hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)

while True:
    h_min = cv.getTrackbarPos('HMin', 'image')
    h_max = cv.getTrackbarPos('HMax', 'image')
    s_min = cv.getTrackbarPos('SMin', 'image')
    s_max = cv.getTrackbarPos('SMax', 'image')
    v_min = cv.getTrackbarPos('VMin', 'image')
    v_max = cv.getTrackbarPos('VMax', 'image')

    lower_bound = np.array([h_min, s_min, v_min])
    upper_bound = np.array([h_max, s_max, v_max])

    mask = cv.inRange(hsv, lower_bound, upper_bound)
    result = cv.bitwise_and(img, img, mask=mask)
    print(f'Lower Bound: {lower_bound}, Upper Bound: {upper_bound}')
    print(h_min, h_max, s_min, s_max, v_min, v_max)
    mask = cv.resize(mask, (800, 400))
    cv.imshow('mask', mask)
    result = cv.resize(result, (800, 400))
    cv.imshow('result', result)

    if cv.waitKey(1) & 0xFF == 27:  # ESC key to exit
        break





cv.waitKey(0)
cv.destroyAllWindows()