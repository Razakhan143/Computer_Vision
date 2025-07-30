import cv2 as cv
import numpy as np

# Load the video
cap = cv.VideoCapture(0)
if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

# Process the video frame by frame
while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Could not read frame.")
        break
    
    frame = cv.resize(frame, (800, 600))
    gray_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    b_w = cv.threshold(gray_frame, 127, 255, cv.THRESH_BINARY)[1]

    # frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    
    cv.imshow('original Camera', frame)
    cv.imshow('Gray Camera', gray_frame)
    cv.imshow('Black and White Camera', b_w)
    if cv.waitKey(25) & 0xFF == ord('q'):
        break
cap.release()
cv.destroyAllWindows()