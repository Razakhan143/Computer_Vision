import os

import cv2

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()
# img = cv2.imread('resources/dogs.jpg')
while True:
    ret, img = cap.read()
    if not ret:
        print("Error: Could not read frame.")
        break

    img = cv2.resize(img, (600, 300))

    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    adaptive_thresh = cv2.adaptiveThreshold(img_gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 21, 30)
    ret, simple_thresh = cv2.threshold(img_gray, 80, 255, cv2.THRESH_BINARY)


    cv2.imshow('img', img)
    cv2.imshow('adaptive_thresh', adaptive_thresh)
    cv2.imshow('simple_thresh', simple_thresh)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    cv2.waitKey(0)
    cv2.destroyAllWindows()