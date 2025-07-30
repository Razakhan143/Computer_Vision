import cv2 as cv
import numpy as np
import os

def find_coord(event, x, y, flags, param):
    if event == cv.EVENT_LBUTTONDOWN:
        print(f"Coordinates: ({x}, {y})")

        font = cv.FONT_HERSHEY_SIMPLEX
        cv.putText(img, f"({x}, {y})", (x, y), font, 0.5, (255, 255, 109), 1, cv.LINE_AA)
        cv.imshow('Finding Coordinates', img)

    if event == cv.EVENT_RBUTTONDOWN:
        print(x,',', y)
        b= img[y, x, 0]
        g= img[y, x, 1]
        r= img[y, x, 2]
        print(f"Color at ({x}, {y}): B={b}, G={g}, R={r}")
        font = cv.FONT_HERSHEY_SIMPLEX
        color = (b, g, r)
        cv.putText(img, f"Color: B={b}, G={g}, R={r}", (x, y + 20), font, 0.5, tuple(map(int, color)), 1, cv.LINE_AA)
        cv.imshow('Finding Coordinates', img)
        cv.waitKey(0)
        cv.destroyAllWindows()


if __name__ == "__main__":
    
    def find_image_file(filename, search_path='.'):
        for root, dirs, files in os.walk(search_path):
            if filename in files:
                return os.path.join(root, filename)
        return None

    # Usage
    image_path = find_image_file('data.jpg')

    if image_path:
        img = cv.imread(image_path)
        if img is not None:
            print(f"Image loaded from: {image_path}")
        else:
            print("Failed to read the image file with OpenCV.")
    else:
        print("Image file not found.")
        if img is None:
            print("❌ Error: Image not found or path is incorrect.")
            exit()

    img = cv.resize(img, (600, 300))
    cv.imshow('Finding Coordinates', img)
    cv.setMouseCallback('Finding Coordinates', find_coord)

    cv.waitKey(0)
    cv.destroyAllWindows()