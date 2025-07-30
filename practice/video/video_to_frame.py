import cv2 as cv
import numpy as np

cap = cv.VideoCapture('cv-lecture1/resources/test.mp4')  # Use 0 for the default camera
frame_no=0
while True:
    ret, frame = cap.read()
    if not ret:
        break
    else:   
        cv.imwrite(f'video/frames/output_{frame_no}.jpg', frame)  # Save the frame to an output file
        frame_no += 1

cap.release()
cv.destroyAllWindows()