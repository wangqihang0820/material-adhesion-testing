import cv2
import numpy as np

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

# from camera1 import *

from custom.graphicsView import *

from config import selectImage_flag


class FileSystemTreeView(QTreeView, QDockWidget):
    def __init__(self, parent=None, graphicsView = None):
        super().__init__(parent=parent)
        self.mainwindow = parent
        self.fileSystemModel = QFileSystemModel()

        #  设置文件根目录
        # self.fileSystemModel.setRootPath("C:\\Users\\12345\Desktop\material-adhesion-testing\workspace")
        # self.setModel(self.fileSystemModel)
        # self.setRootIndex(self.fileSystemModel.index("C:\\Users\\12345\Desktop\material-adhesion-testing\workspace"))
        # 魔法值改为 常量
        self.fileSystemModel.setRootPath(config.WORKSPACE_DIR)
        self.setModel(self.fileSystemModel)
        self.setRootIndex(self.fileSystemModel.index(config.WORKSPACE_DIR))

        # 隐藏size,date等列
        self.setColumnWidth(0, 200)
        self.setColumnHidden(1, True)
        self.setColumnHidden(2, True)
        self.setColumnHidden(3, True)
        # 不显示标题栏
        self.header().hide()
        # 设置动画
        self.setAnimated(True)
        # 选中不显示虚线
        self.setFocusPolicy(Qt.NoFocus)
        #  设置双击 事件
        self.doubleClicked.connect(self.select_image)
        #  设置最小宽度
        self.setMinimumWidth(200)

        #  中间  画布 graphicsView

        self.graphicsView = graphicsView

        # todo 工作目录的增删改查；

        # todo 增加文件夹   改：修改文件名字


        # #  引入照相机
        #
        # self.cc = Camera()
        # self.cc.activatecamera(0)

    """
    
       选择显示图片
    """

    def select_image(self, file_index):
        file_name = self.fileSystemModel.filePath(file_index)

        if config.selectImage_flag == 2:
            self.graphicsView.takeoffCamera()

        config.selectImage_flag = 1

        print("config.selectImage_flag:"+str(config.selectImage_flag))

        if file_name.endswith(('.jpg', '.png', '.bmp')):
            src_img = cv2.imdecode(np.fromfile(file_name, dtype=np.uint8), -1)
            self.mainwindow.change_image(src_img)









