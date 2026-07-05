from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QToolBar, QAction, QLabel
from PyQt5.QtCore import Qt

def display():
    print(123)

def display2():
    print(1234)
app = QApplication([])

# 创建主窗口
window = QWidget()

# # 创建垂直布局管理器
# layout = QVBoxLayout()
#
# # 创建容器
# container = QWidget()
#
# # 创建工具栏
# toolbar = QToolBar()
#
# # 创建动作
# action1 = QAction("Action 1", window)
# action2 = QAction("Action 2", window)
#
# # 将动作添加到工具栏中
# toolbar.addAction(action1)
# toolbar.addAction(action2)
#
# action1.triggered.connect(display)
# action2.triggered.connect(display2)
#
# # 创建标签
# label = QLabel("This is the main content.")
#
# # 创建容器的布局管理器
# containerLayout = QVBoxLayout()
#
# # 将工具栏和标签添加到容器的布局中
# containerLayout.addWidget(toolbar)
# containerLayout.addWidget(label)
#
#
# toolbar.setOrientation(Qt.Vertical)
#
#
# # 设置容器的布局
# container.setLayout(containerLayout)
#
# # 将容器添加到垂直布局中
# layout.addWidget(container)
#
# # 设置主窗口的布局
# window.setLayout(layout)

# 显示主窗口
window.show()

# 运行 QApplication 事件循环
app.exec_()