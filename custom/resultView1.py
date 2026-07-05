from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
# import cv2
from custom.rectangle import rectangle_process
from custom.quxiang import *
from flask import Flask, request, jsonify, send_file
import threading
import json
import cv2
# 代码分别计算硅钢在A,B,C三个区域脱落面积，最后得到等级，属于有取向钢的实验
# app = Flask(__name__)
class resultView1(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # 这里要有mainwindow和src_img的初始化
        self.mainwindow = parent

        self.src_img = None
        self.cur_img = None

        # 创建一个水平布局
        layout = QHBoxLayout()

        # 创建一个按钮
        self.button = QPushButton("处理结果", self)
        self.button.setFixedSize(100, 50)
        font = QFont("NSimSun", 16)
        self.button.setFont(font)

        layout.addWidget(self.button)

        # 创建第一个标签
        self.label1 = QLabel("等级：", self)
        self.label1.setFixedSize(100, 50)
        self.label1.setFont(font)
        layout.addWidget(self.label1)

        # 创建A、B、C三个区域的脱落面积和脱落程度标签
        for i in range(3):
            # 创建一个垂直布局
            vlayout = QVBoxLayout()

            # 创建脱落面积标签
            label2 = QLabel(f"{chr(ord('A') + i)}区脱落等级：", self)
            # label2.setFixedSize(500, 100)
            label2.setFont(font)
            vlayout.addWidget(label2)

            # 创建脱落程度标签
            label3 = QLabel(f"{chr(ord('A') + i)}区脱落面积：", self)
            # label3.setFixedSize(500, 100)
            label3.setFont(font)
            vlayout.addWidget(label3)

            # # 将垂直布局添加到水平布局中
            layout.addLayout(vlayout)

        # 访问第一个垂直布局中的控件
        self.label_level_A = layout.itemAt(2).layout().itemAt(0).widget()
        self.label_ratio_A = layout.itemAt(2).layout().itemAt(1).widget()

        # 访问第二个垂直布局中的控件
        self.label_level_B = layout.itemAt(3).layout().itemAt(0).widget()
        self.label_ratio_B = layout.itemAt(3).layout().itemAt(1).widget()

        # 访问第三个垂直布局中的控件
        self.label_level_C = layout.itemAt(4).layout().itemAt(0).widget()
        self.label_ratio_C = layout.itemAt(4).layout().itemAt(1).widget()

        # 创建一个新按钮
        self.button_2 = QPushButton("重置结果", self)
        self.button_2.setFixedSize(100, 50)
        font = QFont("NSimSun", 16)
        self.button_2.setFont(font)

        layout.addWidget(self.button_2)

        # 将布局设置为窗口的主布局
        self.setLayout(layout)

        # 连接按钮的clicked信号和process_image槽函数
        self.button.clicked.connect(self.process_image)
        self.button_2.clicked.connect(self.reset)

        self.setFixedSize(1200, 100)

    def process_image(self):
        # data = request.get_json()
        # 处理图像的代码
        print("处理图像")
        # image_path = data.get('photoURL')
        # 使用self.mainwindow.trans_img()将图像传输到此处函数

        self.src_img = self.mainwindow.src_img
        self.cur_img = self.mainwindow.cur_img


        if self.src_img is None:
            return

        img = self.src_img.copy()
        #taggled, cropped_img = rectangle_process(img)
        cropped_img = crop_image(img)
        #
        ret, thresh = cv2.threshold(cropped_img, 120, 255, cv2.THRESH_BINARY)

        dropA, rat_A = ratio_A(cropped_img, thresh)
        dropB, rat_B = ratio_B(cropped_img, thresh)
        dropC, rat_C = ratio_C(cropped_img, thresh)

        adhesion_level = measure_adhesion_level(dropA, dropB, dropC)

        # # 输出附着性结果
        print("取向钢涂层附着性等级为：", adhesion_level)

        self.label1.setText(f"等级：{adhesion_level}")

        self.label_level_A.setText(f"A区脱落等级：{dropA}")
        self.label_ratio_A.setText(f"A区脱落面积：{rat_A:.4f}")

        self.label_level_B.setText(f"B区脱落等级：{dropB}")
        self.label_ratio_B.setText(f"B区脱落面积：{rat_B:.4f}")

        self.label_level_C.setText(f"C区脱落等级：{dropC}")
        self.label_ratio_C.setText(f"C区脱落面积：{rat_C:.4f}")

        # print(degradation_level, ratio)

        return adhesion_level


    def reset(self):
        # 将标签上面的值清空
        print("重置结果")

        self.label1.setText(f"等级：")

        self.label_level_A.setText(f"A区脱落等级：")
        self.label_ratio_A.setText(f"A区脱落面积：")

        self.label_level_B.setText(f"B区脱落等级：")
        self.label_ratio_B.setText(f"B区脱落面积：")

        self.label_level_C.setText(f"C区脱落等级：")
        self.label_ratio_C.setText(f"C区脱落面积：")

        return