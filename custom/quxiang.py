# import cv2
# import numpy as np
# from matplotlib import pyplot as plt
# from PyQt5.QtGui import *
# from PyQt5.QtCore import *
# from PyQt5.QtWidgets import *
# import cv2
#
# from functools import partial
# from  custom.rectangle import rectangle_process
#
# import qtawesome as qta
# import sys
#
# def ratio_A(cropped_img,thresh):
#     # 修改的a区脱落面积检测代码
#     # 常量 a 代表左侧起始位置
#     a = 75
#
#     # 计算铁片左侧开头位置
#     # thresh[thresh.shape[0] // 3, :] 表示取图像高度的三分之一位置的那一行，即获取图像中间高度位置的像素值
#     left_edge = int(a / 320 * thresh.shape[1])
#
#     # 计算右侧 15.7mm 的范围
#     right_range = int(15.7 / 320 * thresh.shape[1])
#
#     # 计算右侧区域的像素值 0 和 255 的面积
#     right_area_0 = np.sum(thresh[:, left_edge:left_edge + right_range] == 0)
#     right_area_255 = np.sum(thresh[:, left_edge:left_edge + right_range] == 255)
#
#
#     # 计算面积比值
#     ratio = right_area_255 / (right_area_255 + right_area_0)
#
#     # 在图像中框出铁片左侧区域
#     cv2.rectangle(cropped_img, (left_edge, 0), (left_edge + right_range, thresh.shape[0]), (0, 0, 255), 20)
#     # # 调整窗口大小
#     # cv2.namedWindow('result', cv2.WINDOW_NORMAL)
#     # cv2.resizeWindow('result', 910, 117)
#     #
#     # cv2.imshow('result', cropped_img)
#     # cv2.waitKey(0)
#     # cv2.destroyAllWindows()
#
#
#     def measure_drop(ratio):
#         if ratio <= 0.05:
#             return "无脱落"
#         elif ratio <= 0.25:
#             return "稍有脱落"
#         else:
#             return "脱落"
#
#     drop = measure_drop(ratio)
#
#     # 输出结果
#     print("A区粉尘面积：", right_area_0+right_area_255)
#     print("A区脱落面积：", right_area_255)
#     print("A区脱落面积占总面积比例：", ratio)
#     print("A区脱落程度是:", drop)
#
#     return drop, ratio
#
#
# def ratio_B(cropped_img,thresh):
#     b = 175
#
#     # 计算铁片左侧开头位置
#     left_edge = np.min(np.where(thresh[thresh.shape[0] // 3, :] == 0)) + int(b / 320 * thresh.shape[1])
#
#     # 计算右侧 31.4mm 的范围
#     right_range = int(31.4 / 320 * thresh.shape[1])
#     # 在图像中框出指定范围
#     cv2.rectangle(cropped_img, (left_edge, 0), (left_edge + right_range, thresh.shape[0]), (0, 0, 255), 20)
#
#     # 计算框出区域的总面积
#     total_area = right_range * thresh.shape[0]
#
#     # 计算框出区域内材料脱落的面积
#     fall_off_area = np.sum(thresh[:, left_edge:left_edge + right_range] == 0)
#     fall_off_area_255 = np.sum(thresh[:, left_edge:left_edge + right_range] == 255)
#
#     # 计算面积比值
#     ratio = fall_off_area_255 / (fall_off_area_255 + fall_off_area)
#
#     # # 调整窗口大小
#     # cv2.namedWindow('result', cv2.WINDOW_NORMAL)
#     # cv2.resizeWindow('result', 910, 117)
#     #
#     # cv2.imshow('result', cropped_img)
#     # cv2.waitKey(0)
#     # cv2.destroyAllWindows()
#
#     def measure_drop(ratio):
#         if ratio <= 0.05:
#             return "无脱落"
#         elif ratio <= 0.25:
#             return "稍有脱落"
#         else:
#             return "脱落"
#
#     drop = measure_drop(ratio)
#
#     # 输出结果
#     print("B区粉尘面积：", fall_off_area + fall_off_area_255)
#     print("B区脱落面积：", fall_off_area_255)
#     # print("B区粉尘面积：", right_area_0 + right_area_255)
#     # print("B区脱落面积：", right_area_255)
#     print("B区脱落面积占总面积比例：", ratio)
#     print("B区脱落程度是:", drop)
#
#     return drop, ratio
#
# def ratio_C(cropped_img,thresh):
#     # 常量 c 代表右侧起始位置
#     # 常量 a 代表左侧起始位置
#     a = 245
#
#     # 计算铁片左侧开头位置
#     left_edge = np.min(np.where(thresh[thresh.shape[0] // 3, :] == 0)) + int(a / 320 * thresh.shape[1])
#
#     # 计算右侧 47.1mm 的范围
#     right_range = int(47.1 / 320 * thresh.shape[1])
#     # 在图像中框出指定范围
#     cv2.rectangle(cropped_img, (left_edge, 0), (left_edge + right_range, thresh.shape[0]), (0, 0, 255), 20)
#
#     # 计算框出区域的总面积
#     total_area = right_range * thresh.shape[0]
#
#     # 计算框出区域内材料脱落的面积
#     fall_off_area = np.sum(thresh[:, left_edge:left_edge + right_range] == 0)
#     fall_off_area_255 = np.sum(thresh[:, left_edge:left_edge + right_range] == 255)
#
#     # 计算面积比值
#     ratio = fall_off_area_255 / (fall_off_area_255 + fall_off_area)
#
#     # # 调整窗口大小
#     # cv2.namedWindow('result', cv2.WINDOW_NORMAL)
#     # cv2.resizeWindow('result', 910, 117)
#     #
#     # cv2.imshow('result', cropped_img)
#     # cv2.waitKey(0)
#     # cv2.destroyAllWindows()
#
#     def measure_drop(ratio):
#         if ratio <= 0.05:
#             return "无脱落"
#         elif ratio <= 0.25:
#             return "稍有脱落"
#         else:
#             return "脱落"
#
#     drop = measure_drop(ratio)
#
#     # 输出结果
#     # 输出结果
#     print("C区粉尘面积：", fall_off_area + fall_off_area_255)
#     print("C区脱落面积：", fall_off_area_255)
#     # print("C区粉尘面积：", right_area_0 + right_area_255)
#     # print("C区脱落面积：", right_area_255)
#     print("C区脱落面积占总面积比例：", ratio)
#     print("C区脱落程度是:", drop)
#
#     return drop, ratio
#
# def measure_adhesion_level(dropA, dropB, dropC):
#         if dropA == '无脱落' and dropB == '无脱落':
#             return "A"
#         elif dropA == '稍有脱落' and dropB == '无脱落':
#             return "B"
#         elif dropA == '稍有脱落' and dropB == '稍有脱落':
#             return "C"
#         elif dropA == '脱落' and dropB == '稍有脱落':
#             return "C"
#         elif dropB == '脱落' and dropC == '无脱落':
#             return "D"
#         elif dropB == '脱落' and dropC == '稍有脱落':
#             return "E"
#         elif dropB == '脱落' and dropC == '脱落':
#             return "F"
#
# def crop_image(image):
#     # 获取图像的尺寸
#     height, width = image.shape[:2]
#
#     # 计算裁剪的左上角和右下角坐标
#     left = 0
#     top = 1300
#     right = width
#     bottom = 1700
#
#     # 裁剪图像
#     cropped_image = image[top:bottom, left:right]
#
#     # 返回裁剪后的图像
#     return cropped_image
#
#
#
# if __name__ == '__main__':
#
#     # img_dir = './imgs/33.jpg'
#     #
#     # imgg = cv2.imread(img_dir)
#
#     # cropped_image = crop_image(image)
#     img = crop_image(src_img)
#
#     tagged_img, cropped_img = rectangle_process(img)
#
#     # # 创建窗口
#     # cv2.namedWindow('Cropped Image', cv2.WINDOW_NORMAL)
#     # # 设置窗口大小为910x117像素
#     # cv2.resizeWindow('Cropped Image', 910, 117)
#     # # 显示图像
#     # cv2.imshow('Cropped Image', tagged_img)
#     # # 等待按下任意键
#     # cv2.waitKey(0)
#     # # 关闭窗口
#     # cv2.destroyAllWindows()
#
#     thresh_value = 80
#     ret, thresh = cv2.threshold(cropped_img, thresh_value, 255, cv2.THRESH_BINARY)
#
#     # cv2.namedWindow('Image', cv2.WINDOW_NORMAL)
#     # cv2.resizeWindow('Image', 910, 117)
#     # cv2.imshow('Image', thresh)
#     # cv2.waitKey(0)
#     # cv2.destroyAllWindows()
#
#     dropA, ratio_A = ratio_A(cropped_img, thresh)
#     dropB, ratio_B = ratio_B(cropped_img, thresh)
#     dropC, ratio_C = ratio_C(cropped_img, thresh)
#
#     # 等级评定
#     adhesion_level = measure_adhesion_level(dropA, dropB, dropC)
#
#     # 输出附着性结果
#     print("取向钢涂层附着性等级为：", adhesion_level)

import cv2
import numpy as np
from custom.rectangle import rectangle_process
from matplotlib import pyplot as plt

def ratio_A(cropped_img,thresh):
    # 修改的a区脱落面积检测代码
    # 常量 a 代表左侧起始位置
    a = 30

    # 计算铁片左侧开头位置
    left_edge = np.min(np.where(thresh[thresh.shape[0] // 3, :] == 0)) + int(a / 320 * thresh.shape[1])

    # 计算右侧 15.7mm 的范围
    right_range = int(31.4 / 320 * thresh.shape[1])

    # 计算右侧区域的像素值 0 和 255 的面积
    right_area_0 = np.sum(thresh[:, left_edge:left_edge + right_range] == 0)
    right_area_255 = np.sum(thresh[:, left_edge:left_edge + right_range] == 255)


    # 计算面积比值
    ratio = right_area_255 / (right_area_255 + right_area_0)

    # 在图像中框出铁片左侧区域
    cv2.rectangle(cropped_img, (left_edge, 0), (left_edge + right_range, thresh.shape[0]), (0, 0, 255), 20)
    # 调整窗口大小
    cv2.namedWindow('result', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('result', 910, 117)

    cv2.imshow('result', cropped_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


    def measure_drop(ratio):
        if ratio <= 0.05:
            return "无脱落"
        elif ratio <= 0.25:
            return "稍有脱落"
        else:
            return "脱落"

    drop = measure_drop(ratio)

    # 输出结果
    print("A区粉尘面积：", right_area_0+right_area_255)
    print("A区脱落面积：", right_area_255)
    print("A区脱落面积占总面积比例：", ratio)
    # print("A区脱落程度是:", drop)

    return drop, ratio


def ratio_B(cropped_img,thresh):
    # 修改的b区脱落面积检测代码
    # 常量 a 代表左侧起始位置
    # a = 175
    #
    # # 计算铁片左侧开头位置
    # left_edge = np.min(np.where(thresh[thresh.shape[0] // 3, :] == 0)) + int(a / 320 * thresh.shape[1])
    #
    # # 计算右侧 15.7mm 的范围
    # right_range = int(31.4 / 320 * thresh.shape[1])
    #
    # # 计算右侧区域的像素值 0 和 255 的面积
    # right_area_0 = np.sum(thresh[:, left_edge:left_edge + right_range] == 0)
    # right_area_255 = np.sum(thresh[:, left_edge:left_edge + right_range] == 255)
    #
    #
    # # 计算面积比值
    # ratio = right_area_255 / (right_area_255 + right_area_0)
    #
    # # 在图像中框出铁片左侧区域
    # cv2.rectangle(cropped_img, (left_edge, 0), (left_edge + right_range, thresh.shape[0]), (0, 0, 255), 20)
    b = 170

    # 计算铁片左侧开头位置
    left_edge = np.min(np.where(thresh[thresh.shape[0] // 3, :] == 0)) + int(b / 320 * thresh.shape[1])

    # 计算右侧 15.7mm 的范围
    right_range = int(31.4 / 320 * thresh.shape[1])
    # 在图像中框出指定范围
    cv2.rectangle(cropped_img, (left_edge, 0), (left_edge + right_range, thresh.shape[0]), (0, 0, 255), 20)

    # 计算框出区域的总面积
    total_area = right_range * thresh.shape[0]

    # 计算框出区域内材料脱落的面积
    fall_off_area = np.sum(thresh[:, left_edge:left_edge + right_range] == 0)
    fall_off_area_255 = np.sum(thresh[:, left_edge:left_edge + right_range] == 255)

    # 计算面积比值
    ratio = fall_off_area_255 / (fall_off_area_255 + fall_off_area)

    # 调整窗口大小
    cv2.namedWindow('result', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('result', 910, 117)

    cv2.imshow('result', cropped_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    def measure_drop(ratio):
        if ratio <= 0.05:
            return "无脱落"
        elif ratio <= 0.25:
            return "稍有脱落"
        else:
            return "脱落"

    drop = measure_drop(ratio)

    # 输出结果
    print("B区粉尘面积：", fall_off_area + fall_off_area_255)
    print("B区脱落面积：", fall_off_area_255)
    # print("B区粉尘面积：", right_area_0 + right_area_255)
    # print("B区脱落面积：", right_area_255)
    print("B区脱落面积占总面积比例：", ratio)
    # print("B区脱落程度是:", drop)
    return drop, ratio

def ratio_C(cropped_img,thresh):
    # 常量 c 代表右侧起始位置
    # 常量 a 代表左侧起始位置
    a = 260

    # 计算铁片左侧开头位置
    left_edge = np.min(np.where(thresh[thresh.shape[0] // 3, :] == 0)) + int(a / 320 * thresh.shape[1])

    # 计算右侧 15.7mm 的范围
    right_range = int(15.7 / 320 * thresh.shape[1])
    # 在图像中框出指定范围
    cv2.rectangle(cropped_img, (left_edge, 0), (left_edge + right_range, thresh.shape[0]), (0, 0, 255), 20)

    # 计算框出区域的总面积
    total_area = right_range * thresh.shape[0]

    # 计算框出区域内材料脱落的面积
    fall_off_area = np.sum(thresh[:, left_edge:left_edge + right_range] == 0)
    fall_off_area_255 = np.sum(thresh[:, left_edge:left_edge + right_range] == 255)

    # 计算面积比值
    ratio = fall_off_area_255 / (fall_off_area_255 + fall_off_area)

    # # 计算右侧区域的像素值 0 和 255 的面积
    # right_area_0 = np.sum(thresh[:, left_edge:left_edge + right_range] == 0)
    # right_area_255 = np.sum(thresh[:, left_edge:left_edge + right_range] == 255)
    #
    # # 计算面积比值
    # ratio = right_area_255 / (right_area_255 + right_area_0)
    # # 在图像中框出铁片左侧区域
    # cv2.rectangle(cropped_img, (left_edge, 0), (left_edge + right_range, thresh.shape[0]), (0, 0, 255), 20)
    # 调整窗口大小
    cv2.namedWindow('result', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('result', 910, 117)

    # 输出结果
    print("C区粉尘面积：", fall_off_area + fall_off_area_255)
    print("C区脱落面积：", fall_off_area_255)
    # print("C区粉尘面积：", right_area_0 + right_area_255)
    # print("C区脱落面积：", right_area_255)
    print("C区脱落面积占总面积比例：", ratio)
    # print("C区脱落程度是:", drop)

    cv2.imshow('result', cropped_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    def measure_drop(ratio):
        if ratio <= 0.05:
            return "无脱落"
        elif ratio <= 0.25:
            return "稍有脱落"
        else:
            return "脱落"

    drop = measure_drop(ratio)

    # 输出结果
    # # 输出结果
    # print("C区粉尘面积：", fall_off_area + fall_off_area_255)
    # print("C区脱落面积：", fall_off_area_255)
    # # print("C区粉尘面积：", right_area_0 + right_area_255)
    # # print("C区脱落面积：", right_area_255)
    # print("C区脱落面积占总面积比例：", ratio)
    # # print("C区脱落程度是:", drop)

    return drop, ratio

def measure_adhesion_level(dropA, dropB, dropC):
        if dropA == '无脱落' and dropB == '无脱落':
            return "A"
        elif dropA == '稍有脱落' and dropB == '无脱落':
            return "B"
        elif dropA == '稍有脱落' and dropB == '稍有脱落':
            return "C"
        elif dropA == '脱落' and dropB == '稍有脱落':
            return "C"
        elif dropB == '脱落' and dropC == '无脱落':
            return "D"
        elif dropB == '脱落' and dropC == '稍有脱落':
            return "E"
        elif dropB == '脱落' and dropC == '脱落':
            return "F"
        else:
            return "F"
import cv2
import numpy as np

def crop_image(image):
    # 获取图像的尺寸
    height, width = image.shape[:2]
    # print(height, width)

    # 计算裁剪的左上角和右下角坐标
    left = 0
    top = 1600
    right = width
    bottom = 1975

    # 裁剪图像
    cropped_image = image[top:bottom, left:right]

    # 返回裁剪后的图像
    return cropped_image

if __name__ == '__main__':

    img_dir = r'C:\Users\12345\Desktop\1\material-adhesion-testing\workspace\p1.jpg'
    # img_dir = './imgs/b_xuanzhuan.bmp'

    img = cv2.imread(img_dir)

    # cropped_image = crop_image(image)
    img = crop_image(img)

    # tagged_img, cropped_img = rectangle_process(img)
    #
    # # 创建窗口
    # cv2.namedWindow('Cropped Image', cv2.WINDOW_NORMAL)
    # # 设置窗口大小为910x117像素
    # cv2.resizeWindow('Cropped Image', 910, 117)
    # # 显示图像
    # cv2.imshow('Cropped Image', tagged_img)
    # # 等待按下任意键
    # cv2.waitKey(0)
    # # 关闭窗口
    # cv2.destroyAllWindows()

    ret, thresh = cv2.threshold(img, 120, 255, cv2.THRESH_BINARY)

    dropA, ratio_A = ratio_A(img, thresh)
    dropB, ratio_B = ratio_B(img, thresh)
    dropC, ratio_C = ratio_C(img, thresh)

    # # 等级评定
    # adhesion_level = measure_adhesion_level(dropA, dropB, dropC)
    #
    # # 输出附着性结果
    # print("取向钢涂层附着性等级为：", adhesion_level)

