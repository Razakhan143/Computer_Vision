import cv2 as cv
import numpy as np

# Load the video
cap = cv.VideoCapture(0)
cap.set(10,100)

if not cap.isOpened():
    print("Error: Could not open video.")
    exit()

# Process the video frame by frame
while True:
    ret, frame = cap.read()
    frame = cv.resize(frame, (500, 300))


    if ret == True:
        cv.imshow('Video Frame', frame)
        if cv.waitKey(25) & 0xFF == ord('q'):
            break
    else:
        print("Error: Could not read frame.")
        break
cap.release()
cv.destroyAllWindows()  
  