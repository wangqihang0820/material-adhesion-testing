import cv2
import numpy as np
from matplotlib import pyplot as plt

# 读取图像
image = cv2.imread(r'D:\\CODE\\material-adhesion-testing\\workspace\\data\\20250113114126.jpg')

#自适应窗口大小
cv2.namedWindow('result', cv2.WINDOW_NORMAL)
# cv2.resizeWindow('result', 1000, 500)
cv2.imshow('result', image)

cv2.waitKey(0)  # 等待任意键按下
cv2.destroyAllWindows()  # 关闭所有OpenCV创建的窗口

