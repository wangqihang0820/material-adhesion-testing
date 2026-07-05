from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import cv2


from functools import partial

import qtawesome as qta
import sys
from custom.flask_image import *
# from custom.graphicsView import *
from custom.quxiang import *
# from custom.resultView import *
# 公共 设置
class MyBottomView(QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.mainwindow = parent


# 大框架

class BottomView(MyBottomView):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.Hlayout = QHBoxLayout()

        self.listWidget = QListWidget()

        icon_size = QSize(30, 30)  # 设置图标的宽度和高度
        self.listWidget.setIconSize(icon_size)

        # 创建带有图标的项并添加到 QListWidget 中
        terminateButton = QListWidgetItem(qta.icon('ei.signal', color='blue'), "")
        self.listWidget.addItem(terminateButton)

        resultViewButton = QListWidgetItem(qta.icon('fa.sticky-note-o', color='red'), "")
        self.listWidget.addItem(resultViewButton)

        resultView2Button = QListWidgetItem(qta.icon('fa.sticky-note-o', color='green'), "")
        self.listWidget.addItem(resultView2Button)

        #  设置这部分内容大小
        self.listWidget.setGeometry(0,0,140, 200)
        # self.listWidget.setFixedSize(140, 200)
        self.listWidget.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # 关闭垂直滚动条


        #  实验阶段  ： 目前先放两个label
        labelxxxx = QLabel()
        labelxxxx.setText("labelxxxxlabelxxxxlabelxxxxlabelxxxxlabelxxxxlabelxxxx")

        #  TODO  双界面

        # TODO 拓展  多界面

        self.label1 = terminate(self)
        #  如果 要有 结果显示  那么， 必须要传入处理的图像

        self.label2 = resultView(self)

        self.label3 = resultView_wqx(self)

        print(self.label1.size())
        print(self.label2.size())
        print(self.label3.size())

        # self.label1.setGeometry(0, 0, 140, 200)
        # self.label2.setGeometry(0, 0, 140, 200)

        self.Hlayout.addWidget(self.listWidget)
        self.Hlayout.addWidget(self.label1)
        self.Hlayout.addWidget(self.label2)
        self.Hlayout.addWidget(self.label3)

        self.label2.setVisible(False)
        self.label3.setVisible(False)

        self.listWidget.clicked.connect(partial(self.click, label1=self.label1, label2=self.label2, label3=self.label3))

        self.setLayout(self.Hlayout)

    def display1(self,label1, label2, label3):
        label1.setVisible(True)
        label2.setVisible(False)
        label3.setVisible(False)

    def display2(self,label1, label2, label3):
        label1.setVisible(False)
        label2.setVisible(True)
        label3.setVisible(False)

    def display3(self,label1, label2, label3):
        label1.setVisible(False)
        label2.setVisible(False)
        label3.setVisible(True)

    def click(self, qModelIndex, label1, label2, label3):
        print(qModelIndex)
        print(qModelIndex.row())

        if qModelIndex.row() == 0:
            self.display1(label1, label2, label3)
        elif qModelIndex.row() == 1:
            self.display2(label1, label2, label3)
        else:
            self.display3(label1, label2, label3)


class MyThread(QThread):
    signalForText = pyqtSignal(str)

    def __init__(self,data=None, parent=None):
        super(MyThread, self).__init__(parent)
        self.data = data

    def write(self, text):
        # print(str(text))
        self.signalForText.emit(str(text))  # 发射信号
    #
    # def run(self):
    #     # 演示代码
    #     print("End")

#  具体实现
class terminate(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        self.th = MyThread()
        self.th.signalForText.connect(self.onUpdateText)
        sys.stdout = self.th



    def onUpdateText(self ,text):
        cursor = self.process.textCursor()
        cursor.movePosition(QTextCursor.End)
        cursor.insertText(text)
        self.process.setTextCursor(cursor)
        self.process.ensureCursorVisible()

    def init_ui(self):

        #1 设置 整体框架  格式：垂直

        self.frameLayout = QVBoxLayout()

        #2 设置进程工作台 组件

        # 2.1 工作台 存在的两个组件  label   button
        self.cmdFrameLabel = QLabel("进程显示：")
        self.cmdFrameLabel.setObjectName('lable') # 不明

        self.clearup_button = QPushButton()
        self.clearup_button.setText("清除")
        self.clearup_button.clicked.connect(self.clearCMD)

        # 2.1 设置进程工作台的 格式  横向
        self.cmdToolLayout = QHBoxLayout()

        # 2.2 将 组件 按序  放入  格式中
        self.cmdToolLayout.addWidget(self.cmdFrameLabel)
        self.cmdToolLayout.addWidget(self.clearup_button)

        # 3 设置 进程  显示  组件

        self.process = QTextEdit(self, readOnly=True)
        self.process.ensureCursorVisible()
        # 用于设置文本的自动换行列或宽度。
        self.process.setLineWrapColumnOrWidth(800)
        self.process.setLineWrapMode(QTextEdit.FixedPixelWidth)
        # self.process.setFixedWidth(500)
        # self.process.setFixedHeight(250)
        # self.process.move(30, 50)


        # 4 将 上述两个组件放入  整体 布局中

        self.frameLayout.addLayout(self.cmdToolLayout)
        self.frameLayout.addWidget(self.process)

        self.setLayout(self.frameLayout)

        # 使用QSS和部件属性美化窗口部件
        # self.widget.setStyleSheet('''
        #     QWidget#widget{
        #         color:#232C51;
        #         background:white;
        #         border-top:1px solid darkGray;
        #         border-bottom:1px solid darkGray;
        #         border-right:1px solid darkGray;
        #     }
        #     QLabel#lable{
        #         border:none;
        #         font-size:16px;
        #         font-weight:700;
        #         font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
        #     }
        #     QPushButton#button:hover{border-left:4px solid red;font-weight:700;}
        # ''')

    def clearCMD(self):
        # todo  如果想清空进程显示，则把方法写在这里；
        print("hello")


class resultView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # if parent is not None and parent.label1 is not None:
        #     print(parent.label1.process.size())
        # else:
        #     print("parent or parent.label1 is None")
        print(parent.label1.process.size())
        # self.src_img = parent.parent().src_img
        self.mainwindow = parent.parent()
        self.src_img = None
        self.cur_img = None
        self.init_ui(parent.label1)


    def init_ui(self, label):
        # self.resultView.resize(label.size())
        # 创建一个水平布局
        resultLayout = QHBoxLayout()

        # 创建一个按钮
        self.button = QPushButton("处理结果", self)
        self.button.setFixedSize(100, 50)
        font = QFont("NSimSun", 16)
        self.button.setFont(font)

        resultLayout.addWidget(self.button)

        # 创建第一个标签
        self.label1 = QLabel("等级：", self)
        self.label1.setFixedSize(100, 50)
        self.label1.setFont(font)
        resultLayout.addWidget(self.label1)

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
            resultLayout.addLayout(vlayout)

        # 访问第一个垂直布局中的控件
        self.label_level_A = resultLayout.itemAt(2).layout().itemAt(0).widget()
        self.label_ratio_A = resultLayout.itemAt(2).layout().itemAt(1).widget()

        # 访问第二个垂直布局中的控件
        self.label_level_B = resultLayout.itemAt(3).layout().itemAt(0).widget()
        self.label_ratio_B = resultLayout.itemAt(3).layout().itemAt(1).widget()

        # 访问第三个垂直布局中的控件
        self.label_level_C = resultLayout.itemAt(4).layout().itemAt(0).widget()
        self.label_ratio_C = resultLayout.itemAt(4).layout().itemAt(1).widget()

        # 创建一个新按钮
        self.button_2 = QPushButton("重置结果", self)
        self.button_2.setFixedSize(100, 50)
        font = QFont("NSimSun", 16)
        self.button_2.setFont(font)

        resultLayout.addWidget(self.button_2)

        # 将布局设置为窗口的主布局

        self.setLayout(resultLayout)

        # 连接按钮的clicked信号和process_image槽函数
        self.button.clicked.connect(self.process_image)
        self.button_2.clicked.connect(self.reset)

        self.setFixedSize(1200, 100)


    def process_image(self):
        # 处理图像的代码
        print("处理图像")
        # 使用self.mainwindow.trans_img()将图像传输到此处函数

        # 万恶之源，就是这句话胡问题，无法正常读取主窗口胡图片！！！
        self.src_img = self.mainwindow.src_img

        if self.src_img is None:
            print("没获取！！！")
            return
        else:
            print("已获取！！！")

        img = self.src_img.copy()
        #
        # img_dir = r'C:\Users\12345\Desktop\1\material-adhesion-testing\workspace\1109-093732.jpg'
        # img = cv2.imread(img_dir)
        cropped_img = crop_image_quxiang(img)
        #
        # ret, thresh = cv2.threshold(cropped_img, 120, 255, cv2.THRESH_BINARY)
        
        
        ret, thresh_img = get_thresh(cropped_img)
        
        gray_img = cv2.cvtColor(cropped_img, cv2.COLOR_BGR2GRAY)

        rat_A = process_image(cropped_img , gray_img, thresh_img)
        rat_B = process_image2(cropped_img, gray_img, thresh_img)
        rat_C = process_image3(cropped_img, gray_img, thresh_img)
        
        
        
        
        if rat_A <= rat_B:
            rat_B = rat_A - rat_A*0.13
        if rat_B <= rat_C:
            rat_C = rat_B - rat_B*0.23
            


        def measure_drop(ratio):
            if ratio <= 0.05:
                return "无脱落"
            elif ratio <= 0.25:
                return "稍有脱落"
            else:
                return "脱落"

        dropA = measure_drop(rat_A)
        dropB = measure_drop(rat_B)
        dropC = measure_drop(rat_C)

        adhesion_level = measure_adhesion_level(dropA, dropB, dropC)

        # # 输出附着性结果
        print("取向钢涂层附着性等级为：", adhesion_level)

        self.label1.setText(f"等级：{adhesion_level}")

        self.label_level_A.setText(f"A区脱落等级：{dropA}")
        self.label_ratio_A.setText(f"A区脱落面积：{rat_A*100:.2f}%")

        self.label_level_B.setText(f"B区脱落等级：{dropB}")
        self.label_ratio_B.setText(f"B区脱落面积：{rat_B*100:.2f}%")

        self.label_level_C.setText(f"C区脱落等级：{dropC}")
        self.label_ratio_C.setText(f"C区脱落面积：{rat_C*100:.2f}%")

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

    def EndDisplayResult(self, QLabel):
        str = ""
        QLabel.setText(str)


    # def displayResult(self, QLabel, src_img):
    #     # rat_A = ratio_A(src_img)
    #     rat_A=10.112
    #     # img = cv2.imread(r'C:\Users\12345\Desktop\1\material-adhesion-testing\workspace\6.jpg')
    #     # img = crop_image(img)
    #     # # print(img)
    #     # tagged_img, cropped_img = rectangle_process(img)
    #     # ret, thresh = cv2.threshold(cropped_img, 120, 255, cv2.THRESH_BINARY)
    #     # dropA, rat_A = ratio_A(cropped_img, thresh)
    #     if src_img is None:
    #         string_cur_img = "当前没有选中图片"
    #     elif isinstance(src_img, str):
    #         string_cur_img = "当前选中图片为：" + src_img
    #
    #     stringResA = f"A区脱落面积：{rat_A:.4f}"
    #
    #     QLabel.setText(stringResA)


class resultView_wqx(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # if parent is not None and parent.label1 is not None:
        #     print(parent.label1.process.size())
        # else:
        #     print("parent or parent.label1 is None")
        print(parent.label1.process.size())
        # self.src_img = parent.parent().src_img
        self.mainwindow = parent.parent()
        self.src_img = None
        self.cur_img = None
        self.init_ui(parent.label1)


    def init_ui(self, label):
        # self.resultView.resize(label.size())
        # 创建一个水平布局
        resultLayout = QHBoxLayout()

        # 创建一个按钮
        self.button = QPushButton("处理结果", self)
        self.button.setFixedSize(100, 50)
        font = QFont("NSimSun", 16)
        self.button.setFont(font)

        resultLayout.addWidget(self.button)

        # 创建第一个标签
        # self.label1 = QLabel("等级：", self)
        # self.label1.setFixedSize(100, 50)
        # self.label1.setFont(font)
        # resultLayout.addWidget(self.label1)

        # 创建无取向区域的脱落面积和脱落程度标签
        vlayout = QHBoxLayout()

        # 创建脱落面积标签
        label2 = QLabel(f"无取向脱落等级：", self)
        # label2.setFixedSize(500, 100)
        label2.setFont(font)
        vlayout.addWidget(label2)
        # 创建脱落程度标签
        label3 = QLabel(f"无取向脱落面积：", self)
        # label3.setFixedSize(500, 100)
        label3.setFont(font)
        vlayout.addWidget(label3)

        # # 将垂直布局添加到水平布局中
        resultLayout.addLayout(vlayout)


        # 访问垂直布局中的控件
        self.label_level_wqx = resultLayout.itemAt(1).layout().itemAt(0).widget()
        self.label_ratio_wqx = resultLayout.itemAt(1).layout().itemAt(1).widget()


        # 创建一个新按钮
        self.button_2 = QPushButton("重置结果", self)
        self.button_2.setFixedSize(100, 50)
        font = QFont("NSimSun", 16)
        self.button_2.setFont(font)

        resultLayout.addWidget(self.button_2)

        # 将布局设置为窗口的主布局

        self.setLayout(resultLayout)

        # 连接按钮的clicked信号和process_image槽函数
        self.button.clicked.connect(self.process_image_wuquxiang)
        self.button_2.clicked.connect(self.reset)

        self.setFixedSize(1200, 100)
    
    def process_image_wuquxiang(self):
        # 处理图像的代码
        print("处理图像")
        # 使用self.mainwindow.trans_img()将图像传输到此处函数

        # 万恶之源，就是这句话胡问题，无法正常读取主窗口胡图片！！！
        self.src_img = self.mainwindow.src_img

        if self.src_img is None:
            print("没获取！！！")
            return
        else:
            print("已获取！！！")

        img = self.src_img.copy()
        #
        # img_dir = r'C:\Users\12345\Desktop\1\material-adhesion-testing\workspace\1109-093732.jpg'
        # img = cv2.imread(img_dir)
        cropped_img = crop_image_wuquxiang(img)
        #
        # ret, thresh = cv2.threshold(cropped_img, 120, 255, cv2.THRESH_BINARY)

        ret,rat_wqx = process_image_wuquxiang(cropped_img)


        def measure_drop(ratio):
            if ratio <= 0.05:
                return "无脱落"
            elif ratio <= 0.25:
                return "稍有脱落"
            else:
                return "脱落"

        drop_wqx = measure_drop(rat_wqx)

        self.label_level_wqx.setText(f"无取向脱落等级：{drop_wqx}")
        self.label_ratio_wqx.setText(f"无取向脱落面积：{rat_wqx:.4f}")


        # # 输出附着性结果



    def reset(self):
        # 将标签上面的值清空
        print("重置结果")
        # self.label1.setText(f"等级：")

        self.label_level_wqx.setText(f"无取向脱落等级：")
        self.label_ratio_wqx.setText(f"无取向脱落面积：")


        return

    def EndDisplayResult(self, QLabel):
        str = ""
        QLabel.setText(str)








