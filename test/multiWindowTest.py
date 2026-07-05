import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class Ui_MainWindow(object):
    def __init__(self):
        # 主界面初始化
        self.centralwidget = QtWidgets.QWidget(MainWindow)

        # horizontal_layout = QHBoxLayout()
        #
        self.vertical_layout = QVBoxLayout()

        # self.subCentralwidget = QtWidgets.QWidget(self.centralwidget)


        #   界面布局
        #  两个界面  主界面为  横向布局   其中的一个子界面为垂直布局


        self.HLayout = QHBoxLayout(self.centralwidget)  # 水平布局

        # self.VLayout = QVBoxLayout(self.centralwidget1)  # 垂直布局

        # stackedWidget初始化   切换屏幕插件
        self.stackedWidget = QStackedWidget()

    def setupUi(self, MainWindow):
        # 创建界面
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1440, 773)
        self.centralwidget.setObjectName("centralwidget")
        MainWindow.setCentralWidget(self.centralwidget)

        # # 一级菜单栏布置
        # self.menubar.setGeometry(QtCore.QRect(0, 0, 1440, 24))
        # self.menubar.setObjectName("menubar")
        # self.menu.setObjectName("menu")
        # self.menu_2.setObjectName("menu_2")
        # self.menu_3.setObjectName("menu_3")
        # self.menu_4.setObjectName("menu_4")
        # MainWindow.setMenuBar(self.menubar)
        # # 二级菜单栏布置
        # self.actionRGB_histogram.setObjectName("actionRGB_histogram")
        # self.action.setObjectName("action")
        # self.actionDAISY.setObjectName("actionDAISY")
        # self.actionEHD.setObjectName("actionEHD")
        # self.action_2.setObjectName("action_2")
        # self.actionVGG.setObjectName("actionVGG")
        # self.actionResNet.setObjectName("actionResNet")
        # self.menu.addAction(self.actionRGB_histogram)
        # self.menu_2.addAction(self.action)
        # self.menu_3.addAction(self.actionDAISY)
        # self.menu_3.addAction(self.actionEHD)
        # self.menu_3.addAction(self.action_2)
        # self.menu_4.addAction(self.actionVGG)
        # self.menu_4.addAction(self.actionResNet)
        # self.menubar.addAction(self.menu.menuAction())
        # self.menubar.addAction(self.menu_2.menuAction())
        # self.menubar.addAction(self.menu_3.menuAction())
        # self.menubar.addAction(self.menu_4.menuAction())

        self.HLayout.addLayout(self.vertical_layout) # 水平布局

        # 创建第一个按钮
        self.buttonForFirstForm = QPushButton("处理结果")
        self.buttonForFirstForm.setFixedSize(300, 200)
        font = QFont("NSimSun", 20)
        self.buttonForFirstForm.setFont(font)

        # 创建第二个按钮
        self.buttonForSecondForm = QPushButton("处理结果")
        self.buttonForSecondForm.setFixedSize(300, 200)
        font = QFont("NSimSun", 20)
        self.buttonForSecondForm.setFont(font)

        # self.formLayout.addWidget(self.buttonForFirstForm)
        # self.formLayout.addWidget(self.buttonForSecondForm)

        self.vertical_layout.addWidget(self.buttonForFirstForm)
        self.vertical_layout.addWidget(self.buttonForSecondForm)


        # #  设置 一个容器
        #
        # self.vector = QWidget()
        #
        #
        #
        # # 布局
        #
        # self.HLayout.addWidget(self.vector)

        # 布局添加stackedWidget控件
        self.HLayout.addWidget(self.stackedWidget)


        # self.VLayout.addWidget()

        # 设置主界面面板：
        self.form = QWidget()
        self.formLayout = QVBoxLayout(self.form)  # 水平布局
        self.label0 = QLabel()
        self.label0.setText("主界面！")
        self.label0.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))
        self.label0.setAlignment(Qt.AlignCenter)
        self.label0.setFont(QFont("Roman times", 50, QFont.Bold))
        self.formLayout.addWidget(self.label0)  # 添加控件

        # 设置第1个面板：
        self.form1 = QWidget()
        self.formLayout1 = QHBoxLayout(self.form1)  # 水平布局
        self.label1 = QLabel()
        self.label1.setText("Color")
        self.label1.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))
        self.label1.setAlignment(Qt.AlignCenter)
        self.label1.setFont(QFont("Roman times", 50, QFont.Bold))
        self.formLayout1.addWidget(self.label1)  # 添加控件
        # 设置第2个面板：
        self.form2 = QWidget()
        self.formLayout2 = QHBoxLayout(self.form2)
        self.label2 = QLabel()
        self.label2.setText("Gabor")
        self.label2.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))
        self.label2.setAlignment(Qt.AlignCenter)
        self.label2.setFont(QFont("Roman times", 50, QFont.Bold))
        self.formLayout2.addWidget(self.label2)


        # stackedWidget添加各种界面用于菜单切换
        self.stackedWidget.addWidget(self.form)
        self.stackedWidget.addWidget(self.form1)
        self.stackedWidget.addWidget(self.form2)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        # 窗口名称
        MainWindow.setWindowTitle(_translate("MainWindow", "HZAU实训CBIR系统 @ by ZilanYu"))

        self.buttonForFirstForm.clicked.connect(self.gotoColorWin)
        self.buttonForSecondForm.clicked.connect(self.gotoTexWin)



    # 菜单栏触发每个界面调用函数
    def gotoColorWin(self):
        self.stackedWidget.setCurrentIndex(1)


    def gotoTexWin(self):
        self.stackedWidget.setCurrentIndex(2)


    def gotoDaisyWin(self):
        self.stackedWidget.setCurrentIndex(3)


    def gotoEHDWin(self):
        self.stackedWidget.setCurrentIndex(4)


    def gotoHOGWin(self):
        self.stackedWidget.setCurrentIndex(5)


    def gotoVGGWin(self):
        self.stackedWidget.setCurrentIndex(6)


    def gotoResWin(self):
        self.stackedWidget.setCurrentIndex(7)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())


# from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout, QLabel, QPushButton
#
# app = QApplication([])
#
# # 创建主窗口
# window = QWidget()
#
# # 创建水平布局管理器
# horizontal_layout = QHBoxLayout()
#
# # 创建左边的垂直布局管理器
# vertical_layout = QVBoxLayout()
#
# # 向左边的垂直布局添加部件
# label1 = QLabel("Label 1")
# vertical_layout.addWidget(label1)
#
# button1 = QPushButton("Button 1")
# vertical_layout.addWidget(button1)
#
# # 向水平布局添加左边的垂直布局
# horizontal_layout.addLayout(vertical_layout)
#
# # 添加其他部件到水平布局的右边
# label2 = QLabel("Label 2")
# horizontal_layout.addWidget(label2)
#
# button2 = QPushButton("Button 2")
# horizontal_layout.addWidget(button2)
#
# # 将水平布局设置为主窗口的布局
# window.setLayout(horizontal_layout)
#
# # 显示主窗口
# window.show()
#
# # 运行 QApplication 事件循环
# app.exec_()