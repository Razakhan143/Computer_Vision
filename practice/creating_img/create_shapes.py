import cv2 as cv
import numpy as np

# ones = np.ones((400, 400))
# zeros = np.zeros((400, 400))

# cv.imshow('Ones', ones)
# cv.imshow('Zeros', zeros)
# cv.waitKey(0)
# cv.destroyAllWindows()

img = np.zeros((400, 400, 3), dtype=np.uint8)
img[:] = (125, 255, 123)  # Fill the image with a light yellow color
img[100:300, 100:300] = (255, 255, 255)  # Create a white square in the center
cv.line(img, (400, 400), (200, 0), (255, 0, 255), 10)  # Draw a blue diagonal line
cv.line(img, (0, 0), (400, 400), (0, 0, 255), 5)  # Draw a blue diagonal line
cv.rectangle(img, (50, 50), (350, 350), (255, 0, 0), 3)  # Draw a green rectangle
cv.circle(img, (200, 200), 100, (0, 0, 255), -1)  # Draw a filled red circle
cv.putText(img, 'OpenCV Shapes for the testing purpose of the code', (10, 30), cv.FONT_HERSHEY_SIMPLEX, 0.5, (55, 122, 155), 1)

cv.imshow('white_image.png', img)
# Create a white image of size 400x400 pixels
cv.waitKey(0)
cv.destroyAllWindows()
