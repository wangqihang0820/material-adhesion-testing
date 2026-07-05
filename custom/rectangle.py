import cv2
import numpy as np

def rectangle_process(img):
    # img = cv2.imread("gray.png")
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    ## 边缘检测
    blurred = cv2.blur(gray, (3, 3))
    canny = cv2.Canny(blurred, 50, 200)

    ## find the non-zero min-max coords of canny
    pts = np.argwhere(canny > 0)

    y1, x1 = pts.min(axis=0)
    y2, x2 = pts.max(axis=0)

    ## crop the region
    cropped = gray[y1:y2, x1:x2]

    # cv2.imwrite("cropped.png", cropped)

    ##
    tagged = cv2.rectangle(img.copy(), (x1, y1), (x2, y2), (0, 0, 255), 3, cv2.LINE_AA)

    return tagged, cropped


if __name__ == '__main__':
    # img = cv2.imread("gray.png")
    img_dir = 'C:/Users/12345/Desktop/1/material-adhesion-testing/imgs/e.bmp'
    img = cv2.imread(img_dir)

    rectangle_process(img)
