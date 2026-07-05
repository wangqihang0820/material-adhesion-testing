from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

import matplotlib.pyplot as plt
import numpy as np
import cv2
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from custom.flask_image import *
from custom.flask_image import adaptive_threshold

class histogramView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.mainwindow = parent
        self.src_img = None
        
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        layout = QHBoxLayout()
        self.button = QPushButton("展示", self)
        self.button.setFixedSize(100, 50)
        font = QFont("NSimSun", 12)
        self.button.setFont(font)
        
        self.v_layout = QVBoxLayout()
        self.v_layout.addWidget(self.button)
        self.v_layout.addWidget(self.canvas)
        
        layout.addLayout(self.v_layout)
        self.setLayout(layout)
        
        self.button.clicked.connect(self.histogram)
        # self.setMinimumSize(640, 480)

    # def histogram(self):
    #     self.src_img = self.mainwindow.src_img
    #     if self.src_img is not None:
    #         gray_img = crop_image_quxiang(self.src_img)
    #         otsu_threshold, _ = adaptive_threshold(gray_img)
    #         # 计算灰度图像的直方图
    #         histr = cv2.calcHist([gray_img], [0], None, [256], [0, 256])
    #         histr = histr.flatten()
    #
    #         # 绘制灰度直方图
    #         plt.plot(range(256), histr, color='black')
    #         plt.xlim([0, 256])
    #         plt.grid()
    #         plt.show()
    #
    #     else:
    #         QMessageBox.warning(self, '错误', '请先打开要处理的图片')

    def histogram(self):
        self.src_img = self.mainwindow.src_img
        if self.src_img is not None:
            img = crop_image_quxiang(self.src_img)
            gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            # 计算灰度图像的直方图
            histr = cv2.calcHist([gray_img], [0], None, [256], [0, 256])
            histr = histr.flatten()

            # 绘制灰度直方图
            _= adaptive_threshold(gray_img)
            plt.plot(range(256), histr, color='black')
            plt.axvline(x=_, color='blue', linestyle='--', label=f'Otsu 阈值: {_}')
            plt.xlim([0, 256])
            plt.grid()
            plt.legend()
            plt.show()
        else:
            QMessageBox.warning(self, '错误', '请先打开要处理的图片')


            # def histogram(self):
    #     self.src_img = self.mainwindow.src_img
    #     color = ('b', 'g', 'r')
    #     if self.src_img is not None:
    #         self.figure.clear()
    #         ax = self.figure.add_subplot(111)
    #
    #         for i, col in enumerate(color):
    #             histr = cv2.calcHist([self.src_img], [i], None, [256], [0, 256])
    #             histr = histr.flatten()
    #             ax.plot(range(256), histr, color=col)
    #             ax.set_xlim([0, 256])
    #             ax.grid()
    #
    #         self.canvas.draw()
    #     else:
    #         QMessageBox.warning(self, '错误', '请先打开要处理的图片')

      
        
    # def histogram(self):
    #     color = ('b', 'g', 'r')
    #     if self.src_img is not None:
    #         for i, col in enumerate(color):
    #             histr = cv2.calcHist([self.src_img], [i], None, [256], [0, 256])
    #             histr = histr.flatten()
    #             plt.plot(range(256), histr, color=col)
    #             plt.xlim([0, 256])
    #         plt.show()
    #     else:
    #         QMessageBox.warning(self, '错误', '请先打开要处理的图片')