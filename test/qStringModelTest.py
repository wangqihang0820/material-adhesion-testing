from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QToolBar, QAction, QLabel,QListView,QHBoxLayout,QAbstractItemView, QListWidget, QListWidgetItem
from PyQt5.QtCore import QStringListModel,QSize
from PyQt5.QtGui import  QStandardItemModel,QIcon

from PyQt5.QtCore import Qt

from functools import partial

import qtawesome as qta

def display1(label1,label2):
    label1.setVisible(True)
    label2.setVisible(False)

def display2(label1,label2):
    label1.setVisible(False)
    label2.setVisible(True)

def click1(qModelIndex, label1, label2):
    print(qModelIndex)
    print(qModelIndex.row())

    if qModelIndex.row() == 0:
        display1(label1, label2)
    else:
        display2(label1, label2)


app = QApplication([])

# 创建主窗口
window = QWidget()

Hlayout = QHBoxLayout()

# strList = ["item1", "item2"]
# model = QStringListModel()
# model.setStringList(strList)

#  for  table
# model1 = QStandardItemModel(1,3)
# model2 = QStandardItemModel()

listWidget = QListWidget()

icon_size = QSize(100, 100)  # 设置图标的宽度和高度
listWidget.setIconSize(icon_size)

# 创建带有图标的项并添加到 QListWidget 中
item1 = QListWidgetItem(qta.icon('fa.cloud-download',color='blue'),"")
listWidget.addItem(item1)

item2 = QListWidgetItem(qta.icon('fa.sticky-note-o',color='red'),"")
listWidget.addItem(item2)

listWidget.setFixedSize(140, 200)
listWidget.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # 关闭垂直滚动条

# listWidget.resize(icon_size.width(), 2*listWidget.sizeHintForColumn(0))

# listView = QListView()
# listView.setEditTriggers(QAbstractItemView.NoEditTriggers)
# listView.setModel(model1)
# listViewRight = QListView()

label1 = QLabel()
label1.setText("label1")

label2 = QLabel()
label2.setText("label2")

Hlayout.addWidget(listWidget)
Hlayout.addWidget(label1)
Hlayout.addWidget(label2)

label2.setVisible(False)

listWidget.clicked.connect(partial(click1, label1=label1, label2=label2))

window.setLayout(Hlayout)



# 显示主窗口
window.show()

# 运行 QApplication 事件循环
app.exec_()

