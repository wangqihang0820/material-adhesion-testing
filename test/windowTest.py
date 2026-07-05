from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import matplotlib.pyplot as plt

from custom.stackedWidget import StackedWidget
from custom.treeView import FileSystemTreeView
from custom.listWidgets import FuncListWidget, UsedListWidget
from custom.graphicsView import GraphicsView
from custom.cameraView import CameraView

from camera111 import *

import  sys

class MyApp(QMainWindow):
    def __init__(self):
        super(MyApp, self).__init__()


        # 创建容器 QWidget
        container = QWidget()
        container.resize(400, 300)

        # 创建要重叠的两个组件
        label1 = QLabel("Component 1", container)
        label1.setStyleSheet("background-color: red;")


        label2 = QLabel("Component 2", container)
        label2.setStyleSheet("background-color: blue;")


        self.dock_used = QDockWidget(self)
        self.dock_used.setWidget(label2)

        self.addDockWidget(Qt.LeftDockWidgetArea, self.dock_used)

        self.dock_1 = QDockWidget(self)
        self.dock_1.setWidget(label1)

        self.addDockWidget(Qt.RightDockWidgetArea, self.dock_1)


if __name__ == "__main__":

    app = QApplication(sys.argv)


    window = MyApp()
    window.show()
    sys.exit(app.exec_())