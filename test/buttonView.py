from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton

app = QApplication([])

# 创建主窗口
window = QMainWindow()

# 创建一个容器 QWidget 和布局管理器 QVBoxLayout
central_widget = QWidget()
layout = QVBoxLayout(central_widget)

# 创建要放置在中央部分的组件
label1 = QLabel("Component 1")
label2 = QLabel("Component 2")
label2.hide()  # 初始时隐藏 label2

# 创建一个按钮
button = QPushButton("Toggle Component 2")

# 定义按钮的点击事件的槽函数
def toggle_component2():
    if label2.isVisible():
        label1.show()
        label2.hide()
    else:
        label1.hide()
        label2.show()

button.clicked.connect(toggle_component2)

# 将组件添加到布局中
layout.addWidget(label1)
layout.addWidget(label2)
layout.addWidget(button)

# 将容器设置为主窗口的中央部件
window.setCentralWidget(central_widget)

# 显示主窗口
window.show()

# 运行 QApplication 事件循环
app.exec_()