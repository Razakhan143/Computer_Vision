import cv2 as cv
import numpy as np
# Load the video
cap = cv.VideoCapture(0)
if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()
frame_width = 800
frame_height = 600
out = cv.VideoWriter('cv-lecture1/resources/output.avi', cv.VideoWriter_fourcc(*'XVID'), 20.0, (frame_width, frame_height))
# Process the video frame by frame
while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Could not read frame.")
        break

    frame = cv.resize(frame, (frame_width, frame_height))

    out.write(frame)  # Write the original frame to the video file
    cv.imshow('original Camera', frame)
    if cv.waitKey(25) & 0xFF == ord('q'):
        break
cap.release()
out.release()
cv.destroyAllWindows()