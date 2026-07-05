import cv2
import numpy as np
from rectangle import rectangle_process
from matplotlib import pyplot as plt

def compute_ratio(thresh):

    # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #
    # ## 边缘检测
    # blurred = cv2.blur(gray, (3, 3))
    # canny = cv2.Canny(blurred, 50, 200)
    #
    # ## find the non-zero min-max coords of canny
    # pts = np.argwhere(canny > 0)
    #
    # y1, x1 = pts.min(axis=0)
    # y2, x2 = pts.max(axis=0)
    #
    # ## crop the region
    # cropped = gray[y1:y2, x1:x2]
    #
    # ret, thresh = cv2.threshold(cropped, 120, 255, cv2.THRESH_BINARY)

    print(thresh)

    plt.subplot(1, 1, 1)

    # 计算粉尘面积
    dust_area = np.sum(thresh == 0)

    # 计算脱落面积
    not_stick_area = np.sum(thresh == 255)

    # 计算脱落面积占总面积的比例
    ratio = not_stick_area / (dust_area + not_stick_area)

    def measure_coating_degradation(ratio):
        if ratio <= 0.1:
            return "A"
        else:
            return "B"

    degradation_level = measure_coating_degradation(ratio)

    return degradation_level, ratio