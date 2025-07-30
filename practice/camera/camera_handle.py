import cv2 as cv
import numpy as np

cp = cv.VideoCapture(0)

def resolution(x,y):
    if cp.isOpened():
        cp.set(3, x)  # Set width
        cp.set(4, y)  # Set height
        print(f"Resolution: {int(cp.get(3))}x{int(cp.get(4))}")
    else:
        print("Camera is not opened.")

resolution(640, 480)  # Set resolution to 640x480

while True:
    ret, frame = cp.read()
    if not ret:
        print("Failed to grab frame")
        break

    cv.imshow('Camera Feed', frame)

    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cp.release()
cv.destroyAllWindows()
