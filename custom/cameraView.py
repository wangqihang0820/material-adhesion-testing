import cv2

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from ui_test import *
# from camera111 import Camera


#  显示视频流

class CameraView(QGraphicsView):
    def __init__(self, parent=None,camera= None):

        super(CameraView, self).__init__(parent=parent)
        # 内部类
        self._zoom = 0
        self._empty = True
        self._photo = QGraphicsPixmapItem()
        self._scene = QGraphicsScene(self)

        self._scene.setBackgroundBrush(QColor(Qt.red))

        # self._scene.addItem(self._photo)

        self.setScene(self._scene)
        self.setAlignment(Qt.AlignCenter)  # 居中显示
        self.setDragMode(QGraphicsView.ScrollHandDrag)  # 设置拖动
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setMinimumSize(640, 480)

        self.setVisible(False)
        #
        # # ui
        #
        # self.ui = Ui_MainWindow()
        # self.ui.setupUi(self)
        #
        #
        # ## 照相机 常显
        #
        # self.cam1 = camera
        # self.cam1.activatecamera(0)
        #
        # self.timer_camera = QTimer()
        # self.timer_camera.timeout.connect(self.show_image_on_label)
        # self.timer_camera.start(100)


    def show_image_on_label(self):

        self.image = self.cam1.show_thread()

        # print(type(self.image))
        #
        # print(type(self.image.data))
        #
        # print(self.image.shape)
        #
        # print(self.image.data.shape)

        # show = self.crop_image(self.image, 400, 400)

        show = cv2.resize(self.image, (int(640), int(480)))  # 把读到的帧的大小重新设置为 640x480

        show = show[130:380, :, :]

        show = cv2.cvtColor(show, cv2.COLOR_BGR2RGB)

        # print(show.shape)

        # showImage = QImage(show.data, show.shape[1]-100, show.shape[0]-100, QImage.Format_RGB888)  # 把读取到的视频数据变成QImage形式

        showImage = QImage(show.data, show.shape[1], show.shape[0],
                           QImage.Format_RGB888)  # 把读取到的视频数据变成QImage形式

        self.ui.label.setPixmap(QPixmap.fromImage(showImage))  # 往显示视频的Label里 显示QImage


