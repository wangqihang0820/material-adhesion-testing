import sys
import os
sys.path.append(os.path.abspath(r'C:\Users\12345\Desktop\2\material-adhesion-testing (5)\material-adhesion-testing'))  # 将父目录添加到模块搜索路径中

import os
import numpy as np

import time
from flask import Flask, request, jsonify
import cv2
from custom.resultView1 import *
app = Flask(__name__)
import os
import time
WORKSPACE_DIR = r'D:\\CODE\\material-adhesion-testing\\workspace'

def adaptive_threshold(image):
    # 裁剪三段段用来获取阈值
    image_crop1 = image[:,440:1000]
    image_crop2 = image[:,1670:2300]
    image_crop3 = image[:,3090:]
    # 求三个片段的阈值
    ret1, _ = cv2.threshold(image_crop1, 0, 255, 
                                          cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    ret2, _ = cv2.threshold(image_crop2, 0, 255, 
                                          cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    ret3, _ = cv2.threshold(image_crop3, 0, 255, 
                                          cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    # 求平均
    mean_ret = np.mean([ret1, ret2, ret3])

    return mean_ret


def Save_jpg(image):
    current_date = time.strftime('%Y%m%d', time.localtime())
    folder_path = os.path.join(WORKSPACE_DIR, current_date)
    os.makedirs(folder_path, exist_ok=True)

    # file_path = os.path.join(folder_path, time.strftime('%H%M%S', time.localtime()) + ".jpg")
    
    #从0开始，每300张图片循环覆盖
    existing_files = [f for f in os.listdir(folder_path) if f.endswith('.jpg') and f[:-4].isdigit()]
    if existing_files:
        new_number = (len(existing_files) % 301)
    else:
        new_number = 0
    
    file_path = f"{new_number}.jpg"
    file_path = os.path.join(folder_path, file_path)
    
    cv2.imwrite(file_path, image)
    return file_path




#粗裁剪
def crop_image_quxiang(image):
    # 获取图像的尺寸
    height, width = image.shape[:2]

    # 计算裁剪的左上角和右下角坐标
    left = 40
    top = 1300
    right = 3350
    bottom = 2000

    # 裁剪图像
    cropped_image = image[top:bottom, left:right]
    
    # cv2.namedWindow("cropped_image", cv2.WINDOW_NORMAL)
    # cv2.imshow("cropped_image", cropped_image)
    # 返回裁剪后的图像
    return cropped_image

def edge_queding(thresh,a, b):
    
    # 获取图像尺寸
    height, width = thresh.shape
    x1 = a  
    x2 = b
    x1 = max(0, min(width - 1, x1))
    x2 = max(0, min(width - 1, x2))
    
    y_indices = np.where(thresh[:, x1] == 0)[0]
    if len(y_indices) == 0:
        return None, None
    top_y1 = y_indices[0]
    bottom_y1 = y_indices[-1]
    
    y_indices = np.where(thresh[:, x2] == 0)[0]
    if len(y_indices) == 0:
        return None, None
    top_y2 = y_indices[0]
    bottom_y2 = y_indices[-1]
    
    point1 = (x1, top_y1)
    point2 = (x2, top_y2)
    point3 = (x2, bottom_y2)
    point4 = (x1, bottom_y1)
    
    #output = cropped_img.copy()
    #points = np.array([point1, point2, point3, point4])
    #cv2.polylines(output, [points], isClosed=True, color=(0, 255, 0), thickness=2)
    
    return point1,point2,point3,point4


def crop_image_wuquxiang(image):
    # 获取图像的尺寸

    height, width = image.shape[:2]
    # 计算裁剪的左上角和右下角坐标
    left = 1250
    right = 2700
    # 裁剪图像
    cropped_image = image[:, left:right]

    # 返回裁剪后的图像
    return cropped_image


def get_thresh(image):
    #双边滤波
    denoised_image_bilateral = cv2.bilateralFilter(image, 5, 21, 21)
    gray_image = cv2.cvtColor(denoised_image_bilateral, cv2.COLOR_BGR2GRAY)

    ret = adaptive_threshold(gray_image)
    _, thresh_image = cv2.threshold(gray_image, ret, 255, cv2.THRESH_BINARY)
    # cv2.imshow("equalized_image", gray_image)
    return ret, thresh_image

# def get_thresh(image1,image2):
#     #双边滤波
#     denoised_image_bilateral = cv2.bilateralFilter(image1, 5, 21, 21)
#     gray_image1 = cv2.cvtColor(denoised_image_bilateral, cv2.COLOR_BGR2GRAY)
#     gray_image2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)
#     ret = adaptive_threshold(gray_image1)
#     _, thresh_image = cv2.threshold(gray_image2, ret, 255, cv2.THRESH_BINARY)
#     # cv2.imshow("equalized_image", gray_image)
#     return ret, thresh_image

def ratio_wuquxiang(cropped_img, thresh, a, b, c, d):
    left_edge = a
    right_range = b
    top = c
    bottom = d

    # 在图像中框出指定区域

    cv2.rectangle(cropped_img, (left_edge, c), (left_edge + right_range, d), (0, 0, 255), 20)

    # 计算指定区域的像素值0和255的面积
    area_0 = np.sum(thresh[c:d, left_edge:left_edge + right_range] == 0)
    area_255 = np.sum(thresh[c:d, left_edge:left_edge + right_range] == 255)

    # 计算面积比值
    ratio_wqx = area_0 / (area_255 + area_0)

    ########测试部分
    

    cv2.namedWindow('result', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('result', 390, 768)
    cv2.imshow('result', cropped_img)
    cv2.namedWindow('thresh_result', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('thresh_result', 390, 768)
    cv2.imshow('thresh_result', thresh)

    print("0的个数", area_0)
    print("255的个数", area_255)

    #########

    # 输出结果
    print("脱落面积占总面积比例：", ratio_wqx)

    return ratio_wqx

def ratio_A(cropped_img, gray_img, thresh, a, b):
    
    points = edge_queding(thresh, a, b)
    for point in points:
        if point is None:
            return -1
    if points:
        point1, point2, point3, point4 = points

        mask = np.zeros(cropped_img.shape[:2], dtype=np.uint8)
        poly_points = np.array([point1, point2, point3, point4], np.int32)
        cv2.fillPoly(mask, [poly_points], 255)
        cv2.polylines(cropped_img, [poly_points], isClosed=True, color=(0, 0, 255), thickness=10)
        
    
    total_pixel = np.sum(mask > 0)
    white_pixels = np.sum((thresh == 255) & (mask > 0))
    

    # 计算面积比值
    ratio = white_pixels / total_pixel


    ########测试部分
    thresh = cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR)
    #gray_img = cv2.cvtColor(gray_img, cv2.COLOR_GRAY2BGR)
    conbine_img = cv2.vconcat([cropped_img, thresh])
    cv2.namedWindow('result', cv2.WINDOW_NORMAL)
    cv2.imshow('result', conbine_img)

    # cv2.namedWindow('result', cv2.WINDOW_NORMAL)
    # cv2.resizeWindow('result', 910, 117)
    # cv2.imshow('result', cropped_img)
    # cv2.namedWindow('thresh_result', cv2.WINDOW_NORMAL)
    # cv2.resizeWindow('thresh_result', 910, 117)
    # cv2.imshow('thresh_result', thresh)

    print("总的个数",total_pixel)
    print("脱落点个数",white_pixels)

    # 输出结果
    print("A区脱落面积占总面积比例：", ratio)

    return ratio


def ratio_B(cropped_img, gray_img, thresh, a, b):
    points = edge_queding(thresh, a, b)
    for point in points:
        if point is None:
            return -1
    if points:
        point1, point2, point3, point4 = points

        mask = np.zeros(cropped_img.shape[:2], dtype=np.uint8)
        poly_points = np.array([point1, point2, point3, point4], np.int32)
        cv2.fillPoly(mask, [poly_points], 255)
        cv2.polylines(cropped_img, [poly_points], isClosed=True, color=(0, 0, 255), thickness=10)
        
    total_pixel = np.sum(mask > 0)
    white_pixels = np.sum((thresh == 255) & (mask > 0))
    


    # 在图像中框出指定区域

    #cv2.rectangle(cropped_img, (left_edge, 0), (left_edge + right_range, cropped_img.shape[0]), (0, 0, 255), 20)
    
    

    # 计算指定区域的像素值0和255的面积
    #area_0 = np.sum(thresh[:, left_edge:left_edge + right_range] == 0)
    #area_255 = np.sum(thresh[:, left_edge:left_edge + right_range] == 255)

    # 计算面积比值
    ratio = white_pixels / total_pixel


    ########测试部分
    thresh = cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR)
    #gray_img = cv2.cvtColor(gray_img, cv2.COLOR_GRAY2BGR)
    conbine_img = cv2.vconcat([cropped_img, thresh])
    cv2.namedWindow('result', cv2.WINDOW_NORMAL)
    cv2.imshow('result', conbine_img)
    

    # cv2.namedWindow('result', cv2.WINDOW_NORMAL)
    # cv2.resizeWindow('result', 910, 117)
    # cv2.imshow('result', cropped_img)
    # cv2.namedWindow('thresh_result', cv2.WINDOW_NORMAL)
    # cv2.resizeWindow('thresh_result', 910, 117)
    # cv2.imshow('thresh_result', thresh)

    print("总的个数",total_pixel)
    print("脱落点个数",white_pixels)

    # 输出结果
    print("B区脱落面积占总面积比例：", ratio)

    return ratio


def ratio_C(cropped_img, gray_img, thresh, a, b):
    # 计算区域的左侧边缘和宽度
    points = edge_queding(thresh, a, b)
    for point in points:
        if point is None:
            return -1
    if points:
        point1, point2, point3, point4 = points

        mask = np.zeros(cropped_img.shape[:2], dtype=np.uint8)
        poly_points = np.array([point1, point2, point3, point4], np.int32)
        cv2.fillPoly(mask, [poly_points], 255)
        cv2.polylines(cropped_img, [poly_points], isClosed=True, color=(0, 0, 255), thickness=10)
                
    total_pixel = np.sum(mask > 0)
    white_pixels = np.sum((thresh == 255) & (mask > 0))
    
    

    # 在图像中框出指定区域

    #cv2.rectangle(cropped_img, (left_edge, 0), (left_edge + right_range, cropped_img.shape[0]), (0, 0, 255), 20)
    
    

    # 计算指定区域的像素值0和255的面积
    #area_0 = np.sum(thresh[:, left_edge:left_edge + right_range] == 0)
    #area_255 = np.sum(thresh[:, left_edge:left_edge + right_range] == 255)

    # 计算面积比值
    ratio = white_pixels / total_pixel


    ########测试部分
    thresh = cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR)
    #gray_img = cv2.cvtColor(gray_img, cv2.COLOR_GRAY2BGR)
    conbine_img = cv2.vconcat([cropped_img, thresh])
    cv2.namedWindow('result', cv2.WINDOW_NORMAL)
    cv2.imshow('result', conbine_img)

    # cv2.namedWindow('result', cv2.WINDOW_NORMAL)
    # cv2.resizeWindow('result', 910, 117)
    # cv2.imshow('result', cropped_img)
    # cv2.namedWindow('thresh_result', cv2.WINDOW_NORMAL)
    # cv2.resizeWindow('thresh_result', 910, 117)
    # cv2.imshow('thresh_result', thresh)

    print("总的个数",total_pixel)
    print("脱落点个数",white_pixels)

    # 输出结果
    print("C区脱落面积占总面积比例：", ratio)

    return ratio


def process_image(image, gray_img, thresh_img):

    rat_A = ratio_A(image, gray_img, thresh_img, 180, 480)

    return rat_A

def process_image2(image, gray_img, thresh):

    rat_B = ratio_B(image, gray_img, thresh, 1250, 1750)

    return rat_B

def process_image3(image, gray_img, thresh):

    rat_C = ratio_C(image, gray_img, thresh, 2395, 3075)

    return rat_C

def process_image_wuquxiang(image):

    ret, thresh = get_thresh(image)
    # print("#"*100,ret)
    rat_wqx = ratio_wuquxiang(image, thresh, 170, 1152, 1080, 2838)

    #是否脱落结果
    # return dropA
    return ret, rat_wqx
#-----------------------------------------------------

# @app.route('/process_image', methods=['POST'])
# def handle_process_image():
#     data = request.get_json()
#     _type = data.get('type')
#     _photograph = data.get('photograph')

#     # 初始化结果变量
#     value10, value20, value30, image_path = None, None, None, None

#     # 初始化默认的响应数据
#     response_data = {
#         "photograph": "not processed",
#         "value10": "N/A",
#         "value20": "N/A",
#         "value30": "N/A",
#         "imagePath": "N/A"
#     }

#     if _type == "ori":
#         if _photograph == "ask":
#             # 执行拍照操作或者相关处理

#             print("点击，相机连接")

#             ## 激活相机
#             cc = Camera()
#             cc.activatecamera(1)
#             print("激活，相机")
#             image = cc.show_thread()
#             cc.closedevice()
#             # image_path = Save_jpg(image)
#             # print("#"*100)
#             # print(image)
#             # # cv2.imshow("123",image)
#             # exit()
#             # process_image(image)

#             # cc.takeshot()

#             # 假设获取到的结果
#             value10 = "dropA"
#             value20 = "dropB"
#             value30 = "dropC"
#             # image_path = Save_jpg(image)
#             print(image.shape)
#             # 将保存的图片进行裁剪
#             image = crop_image_quxiang(image)
#             # image_path = Save_jpg(image)
#             print(image.shape)
#             # image_path = "./img/result_image.jpg"

#             _photograph = "ok"
#             # 构建响应数据

#             # 处理图片并保存结果
#             resultA = process_image(image)
#             resultB = process_image2(image)
#             ret, resultC = process_image3(image)
#             # 旋转图像180度
#             # rotated_image = cv2.rotate(image, cv2.ROTATE_180)
#             # 保存旋转后的图像
#             # image_path = Save_jpg(rotated_image)
#             image_path = Save_jpg(image)

#             response_data = {
#                 "photograph": _photograph,
#                 "value10": resultA,
#                 "value20": resultB,
#                 "value30": resultC,
#                 "imagePath": image_path,
#                 'ret_threshold': ret
#             }

#             return jsonify(response_data)  # 使用 jsonify 发送响应

#     elif _type == "nonOri":
#         if _photograph == "ask":
#             # 执行拍照操作或者相关处理

#             print("点击，相机连接")

#             ## 激活相机
#             cc = Camera()
#             cc.activatecamera(0)
#             print("激活，相机")
#             image = cc.show_thread()
#             cc.closedevice()
#             # image_path = Save_jpg(image)
#             # print("#"*100)
#             # print(image)
#             # # cv2.imshow("123",image)
#             # exit()
#             # process_image(image)

#             # cc.takeshot()

#             # 假设获取到的结果
#             value10 = "dropA"
#             # image_path = Save_jpg(image)
#             print(image.shape)
#             # 裁剪前保存原图
#             # image_path = Save_jpg(image)
#             # 将保存的图片进行裁剪
#             image = crop_image_wuquxiang(image)

#             print(image.shape)
#             # image_path = "./img/result_image.jpg"

#             _photograph = "ok"
#             # 构建响应数据
#             ret_wqx,result_wuquxiang = process_image_wuquxiang(image)
#             # 保存处理后的图片
#             image_path = Save_jpg(image)

#             response_data = {
#                 "photograph": _photograph,
#                 "value10": result_wuquxiang,
#                 "imagePath": image_path,
#                 "ret_threshold": ret_wqx,
#             }
#             return jsonify(response_data)  # 使用 jsonify 发送响应

#             # # 执行拍照操作或者相关处理
#             # _photograph = "ok"  # 标记为已拍照
#             # # 假设获取到的结果
#             # value10 = "40"
#             # value20 = "50"
#             # value30 = "60"
#             # image_path = "./img/result_image.jpg"
#             #
#             # # 构建响应数据
#             # response_data = {
#             #     "photograph": _photograph,
#             #     "value10": value10,
#             #     "value20": value20,
#             #     "value30": value30,
#             #     "imagePath": image_path
#             # }
#             #
#             # return jsonify(response_data)  # 使用 jsonify 发送响应


# def run_flask_app():
#     app.run("192.168.0.100", port=5000, debug=True, use_reloader=False)

# 在实际部署时，可以直接调用 run_flask_app() 函数来启动服务
# 这里注释掉，因为在实际脚本执行环境中无法运行 Flask 服务器
# run_flask_app()
