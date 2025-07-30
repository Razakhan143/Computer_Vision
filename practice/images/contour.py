import os

import cv2


img = cv2.imread('resources/birdswhite.jpg')
img = cv2.resize(img, (1000, 600))
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

ret, thresh = cv2.threshold(img_gray, 200, 255, cv2.THRESH_BINARY_INV)

contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

for cnt in contours:
    if cv2.contourArea(cnt) > 200:
        # cv2.drawContours(img, cnt, -1, (0, 255, 0), 1)

        x1, y1, w, h = cv2.boundingRect(cnt)

        cv2.rectangle(img, (x1, y1), (x1 + w, y1 + h), (0, 255, 0), 2)

cv2.imshow('img', img)
cv2.imshow('thresh', thresh)
cv2.waitKey(0)














# import cv2

# # Capture video from webcam
# cap = cv2.VideoCapture(0)
# if not cap.isOpened():
#     print("Error: Could not open camera.")
#     exit()

# while True:
#     ret, frame = cap.read()
#     if not ret:
#         print("Error: Could not read frame.")
#         break

#     # Resize frame
#     frame = cv2.resize(frame, (800, 600))

#     # Convert to grayscale
#     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

#     # Thresholding
#     _, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)

#     # Find contours
#     contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

#     for cnt in contours:
#         if cv2.contourArea(cnt) > 200:
#             x, y, w, h = cv2.boundingRect(cnt)
#             cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

#     # Display the frames
#     cv2.imshow('Frame', frame)
#     cv2.imshow('Threshold', thresh)

#     # Exit on pressing 'q'
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# # Release everything properly
# cap.release()
# cv2.destroyAllWindows()
