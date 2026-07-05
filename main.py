import sys
import cv2
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import matplotlib.pyplot as plt
import qdarkstyle
from qdarkstyle import LightPalette



from custom.stackedWidget import StackedWidget
from custom.treeView import FileSystemTreeView
from custom.listWidgets import FuncListWidget, UsedListWidget
from custom.graphicsView import GraphicsView
from custom.bottomView import BottomView
from custom.histogramView import histogramView
from custom.flask_image import *

from flask import Flask, request, jsonify, send_file
import threading
import json
import cv2
from custom import resultView1

#  目前不用
# from custom.resultView import  resultView


##  暂时不用
from custom.cameraView import CameraView

# from camera1 import *

from  config import  selectImage_flag
app1 = Flask(__name__)
class MyApp(QMainWindow):
    def __init__(self):
        super(MyApp, self).__init__()

        """
            照相机
        """

        # self.cc = Camera()

        #

        self.src_img = None

        #

        self.cur_img = None

        """
            工具栏
        
        """

        #   TODO 工具栏格式调整

        self.tool_bar = self.addToolBar('工具栏')
        self.action_right_rotate = QAction(QIcon("icons/右旋转.png"), "向右旋转90", self)
        self.action_left_rotate = QAction(QIcon("icons/左旋转.png"), "向左旋转90°", self)
        self.action_histogram = QAction(QIcon("icons/直方图.png"), "直方图", self)
        #   用connect绑定事件

        self.action_right_rotate.triggered.connect(self.right_rotate)
        self.action_left_rotate.triggered.connect(self.left_rotate)
        self.action_histogram.triggered.connect(self.histogram)

        self.tool_bar.addActions((self.action_left_rotate, self.action_right_rotate, self.action_histogram))

        """
            引入组件
        """

        # 需要引入照相机
        self.graphicsView = GraphicsView(self)

        self.useListWidget = UsedListWidget(self)

        # 需要引入照相机
        self.funcListWidget = FuncListWidget(self, graphicsView= self.graphicsView)

        self.stackedWidget = StackedWidget(self)


        # 引入 中间 画布
        self.fileSystemTreeView = FileSystemTreeView(self, graphicsView= self.graphicsView)


        self.bottomView = BottomView(self)


        # 引入直方图
        self.histogramView = histogramView(self)

        # # 需要引入照相机
        # self.cameraView = CameraView(self, camera=self.cc)


        """
            主界面 展示 格式
        """

        self.dock_file = QDockWidget(self)
        self.dock_file.setWidget(self.fileSystemTreeView)
        self.dock_file.setTitleBarWidget(QLabel('工作目录'))
        self.dock_file.setFeatures(QDockWidget.NoDockWidgetFeatures)

        self.dock_func = QDockWidget(self)
        self.dock_func.setWidget(self.funcListWidget)
        self.dock_func.setTitleBarWidget(QLabel('图像操作'))
        self.dock_func.setFeatures(QDockWidget.NoDockWidgetFeatures)

        self.dock_used = QDockWidget(self)
        self.dock_used.setWidget(self.useListWidget)
        self.dock_used.setTitleBarWidget(QLabel('已选操作'))
        self.dock_used.setFeatures(QDockWidget.NoDockWidgetFeatures)

        self.dock_his = QDockWidget(self)
        self.dock_his.setWidget(self.histogramView)
        self.dock_his.setTitleBarWidget(QLabel('直方图展示'))
        self.dock_his.setFeatures(QDockWidget.NoDockWidgetFeatures)

        self.dock_attr = QDockWidget(self)
        self.dock_attr.setWidget(self.stackedWidget)
        self.dock_attr.setTitleBarWidget(QLabel('属性'))
        self.dock_attr.setFeatures(QDockWidget.NoDockWidgetFeatures)
        # 设置默认 不显示
        self.dock_attr.close()


        self.dock_bottom = QDockWidget(self)
        # self.dock_bottom.setWidget(self.resultView)
        self.dock_bottom.setWidget(self.bottomView)
        self.dock_bottom.setTitleBarWidget(QLabel('检测系统'))
        self.dock_bottom.setFeatures(QDockWidget.NoDockWidgetFeatures)


        """
            组件摆放位置
        """

        self.setCentralWidget(self.graphicsView)
        # self.setCentralWidget(self.cameraView)



        self.addDockWidget(Qt.LeftDockWidgetArea, self.dock_file)
        self.addDockWidget(Qt.TopDockWidgetArea, self.dock_func)
        self.addDockWidget(Qt.RightDockWidgetArea, self.dock_used)
        self.addDockWidget(Qt.RightDockWidgetArea, self.dock_attr)
        self.addDockWidget(Qt.BottomDockWidgetArea, self.dock_bottom)
        self.addDockWidget(Qt.RightDockWidgetArea, self.dock_his)



        """
            界面
        """

        self.setWindowTitle('Opencv图像处理')
        self.setWindowIcon(QIcon('icons/main.png'))





    # 修改图片

    def trans_img(self):
        if self.src_img is None:
            return
        else:
            return self.src_img

    def update_image(self):
        if self.src_img is None:
            return
        img = self.process_image()
        self.cur_img = img
        self.graphicsView.update_image(img)

    def change_image(self, img):
        self.src_img = img
        img = self.process_image()
        self.cur_img = img
        self.graphicsView.change_image(img)

    def process_image(self):
        img = self.src_img.copy()
        for i in range(self.useListWidget.count()):



            img = self.useListWidget.item(i)(img)

            #img = self.useListWidget.item(i)(img)

        return img

    # 右旋转 实现

    def right_rotate(self):
        self.graphicsView.rotate(90)

    # 左旋转 实现

    def left_rotate(self):
        self.graphicsView.rotate(-90)

    #  直方图

    def histogram(self):
        if self.src_img is not None:
            gray_img = crop_image_quxiang(self.src_img)
            # 计算灰度图像的直方图
            histr = cv2.calcHist([gray_img], [0], None, [256], [0, 256])
            histr = histr.flatten()

            # 绘制灰度直方图
            plt.plot(range(256), histr, color='black')
            plt.xlim([0, 256])
            plt.show()
        else:
            QMessageBox.warning(self, '错误', '请先打开要处理的图片')


    # @app1.route('/process_image', methods=['POST'])
    # def handle_process_image(self):
    #     data = request.get_json()
    #     # 假设你的图像处理函数需要这样的输入
    #     image_path = data.get('photoURL')
    #     # 图像处理逻辑...
    #     # 比如调用 resultView1 的某个实例来处理图像并获取结果
    #     result_view_instance = resultView1()
    #     result_view_instance.src_img = cv2.imread(image_path)
    #     adhesion_level = result_view_instance.process_image()
    #
    #     # 创建要返回的 JSON 数据
    #     response_data = {
    #         "type": data.get("type", "nonOrientation"),
    #         "photograph": data.get("photograph", "ok"),
    #         "value10": data.get("value10", -1),
    #         "value20": data.get("value20", -1),
    #         "value30": data.get("value30", -1),
    #         "photoURL": image_path,  # 或者处理后的图像路径
    #         "adhesion_level": adhesion_level
    #     }
    #
    #     return jsonify(response_data)
    #
    # # def run_flask_app(self):
    # def run_flask_app(self):
    #     app.run(port=5000, debug=True, use_reloader=False)


if __name__ == "__main__":
    # myapp1=MyApp()

    # flask_thread = threading.Thread(target=run_flask_app)
    # flask_thread.start()
    app = QApplication(sys.argv)


    # 创建一个字体
    font = QFont("NSimSun")
    font.setPointSize(12)
    # 设置全局字体
    app.setFont(font)

    # 样式
    # app.setStyleSheet(open('./custom/styleSheet.qss', encoding='utf-8').read())

    app.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt5', palette=LightPalette()))

    window = MyApp()
    window.showMaximized()


    window.show()
    # app1.run(port=5000, debug=True, use_reloader=False,threaded=True)



    sys.exit(app.exec_())

