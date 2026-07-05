from custom.tableWidget import *
from custom.listWidgetItems import *
from custom.bottomView import *


# Implemented functions
items = [
    GrayingItem,
    FilterItem,
    EqualizeItem,
    MorphItem,
    GradItem,
    ThresholdItem,
    EdgeItem,
    ContourItem,
    HoughLineItem,
    LightItem,
    GammaItem,
    CameraLink,
    TakePhotoItem,
]

tables = [
    GrayingTableWidget,
    FilterTabledWidget,
    EqualizeTableWidget,
    MorphTabledWidget,
    GradTabledWidget,
    ThresholdTableWidget,
    EdgeTableWidget,
    ContourTableWidget,
    HoughLineTableWidget,
    LightTableWidget,
    GammaITabelWidget
]


#  照片  工作路径
WORKSPACE_DIR  =  "workspace/"

# 判断 当前是否有选中图片

"""
    0  中间什么都不显示 --- 默认状态
    1  则图片显示在视频流上方 ---显示图片
    2  则图片显示在视频流下方 ---显示视频
"""

selectImage_flag  = 0



"""
    目前只做了  两个显示
    
    一个是   终端显示    terminate
    另一个是    结果显示    resultView
"""


#  下方  结果显示

bottomView = [
    terminate,
    resultView,
]


