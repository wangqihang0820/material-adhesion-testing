import numpy as np
import threading

from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon, QColor
from PyQt5.QtWidgets import QListWidgetItem, QPushButton, QMainWindow
from flags import *
# from camera import *


# from functionCode.CameraParams_header import *
# from functionCode.MvCameraControl_class import *
# from functionCode.PixelType_header import *



class MyItem(QListWidgetItem):
    def __init__(self, name=None, parent=None):
        super(MyItem, self).__init__(name, parent=parent)
        self.setIcon(QIcon('icons/color.png'))
        self.setSizeHint(QSize(60, 60))  # size

    def get_params(self):
        protected = [v for v in dir(self) if v.startswith('_') and not v.startswith('__')]
        param = {}
        for v in protected:
            param[v.replace('_', '', 1)] = self.__getattribute__(v)
        return param

    def update_params(self, param):
        for k, v in param.items():
            if '_' + k in dir(self):
                self.__setattr__('_' + k, v)


class GrayingItem(MyItem):
    def __init__(self, parent=None):
        super(GrayingItem, self).__init__(' 灰度化 ', parent=parent)
        self._mode = BGR2GRAY_COLOR

    def __call__(self, img):
        img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        return img


class FilterItem(MyItem):

    def __init__(self, parent=None):
        super().__init__('平滑处理', parent=parent)
        self._ksize = 3
        self._kind = MEAN_FILTER
        self._sigmax = 0

    def __call__(self, img):
        if self._kind == MEAN_FILTER:
            img = cv2.blur(img, (self._ksize, self._ksize))
        elif self._kind == GAUSSIAN_FILTER:
            img = cv2.GaussianBlur(img, (self._ksize, self._ksize), self._sigmax)
        elif self._kind == MEDIAN_FILTER:
            img = cv2.medianBlur(img, self._ksize)
        return img


class MorphItem(MyItem):
    def __init__(self, parent=None):
        super().__init__(' 形态学 ', parent=parent)
        self._ksize = 3
        self._op = ERODE_MORPH_OP
        self._kshape = RECT_MORPH_SHAPE

    def __call__(self, img):
        op = MORPH_OP[self._op]
        kshape = MORPH_SHAPE[self._kshape]
        kernal = cv2.getStructuringElement(kshape, (self._ksize, self._ksize))
        img = cv2.morphologyEx(img, self._op, kernal)
        return img


class GradItem(MyItem):

    def __init__(self, parent=None):
        super().__init__('图像梯度', parent=parent)
        self._kind = SOBEL_GRAD
        self._ksize = 3
        self._dx = 1
        self._dy = 0

    def __call__(self, img):
        if self._dx == 0 and self._dy == 0 and self._kind != LAPLACIAN_GRAD:
            self.setBackground(QColor(255, 0, 0))
            self.setText('图像梯度 （无效: dx与dy不同时为0）')
        else:
            self.setBackground(QColor(200, 200, 200))
            self.setText('图像梯度')
            if self._kind == SOBEL_GRAD:
                img = cv2.Sobel(img, -1, self._dx, self._dy, self._ksize)
            elif self._kind == SCHARR_GRAD:
                img = cv2.Scharr(img, -1, self._dx, self._dy)
            elif self._kind == LAPLACIAN_GRAD:
                img = cv2.Laplacian(img, -1)
        return img


class ThresholdItem(MyItem):
    def __init__(self, parent=None):
        super().__init__('阈值处理', parent=parent)
        self._thresh = 127
        self._maxval = 255
        self._method = BINARY_THRESH_METHOD

    def __call__(self, img):
        method = THRESH_METHOD[self._method]
        img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        img = cv2.threshold(img, self._thresh, self._thresh, method)[1]
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        return img


class EdgeItem(MyItem):
    def __init__(self, parent=None):
        super(EdgeItem, self).__init__('边缘检测', parent=parent)
        self._thresh1 = 20
        self._thresh2 = 100

    def __call__(self, img):
        img = cv2.Canny(img, threshold1=self._thresh1, threshold2=self._thresh2)
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        return img


class ContourItem(MyItem):
    def __init__(self, parent=None):
        super(ContourItem, self).__init__('轮廓检测', parent=parent)
        self._mode = TREE_CONTOUR_MODE
        self._method = SIMPLE_CONTOUR_METHOD
        self._bbox = NORMAL_CONTOUR

    def __call__(self, img):
        mode = CONTOUR_MODE[self._mode]
        method = CONTOUR_METHOD[self._method]
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        cnts, _ = cv2.findContours(img, mode, method)
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        if self._bbox == RECT_CONTOUR:
            bboxs = [cv2.boundingRect(cnt) for cnt in cnts]
            print(bboxs)
            for x, y, w, h in bboxs:
                img = cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), thickness=2)
        elif self._bbox == MINRECT_CONTOUR:
            bboxs = [np.int0(cv2.boxPoints(cv2.minAreaRect(cnt))) for cnt in cnts]
            img = cv2.drawContours(img, bboxs, -1, (255, 0, 0), thickness=2)
        elif self._bbox == MINCIRCLE_CONTOUR:
            circles = [cv2.minEnclosingCircle(cnt) for cnt in cnts]
            print(circles)
            for (x, y), r in circles:
                img = cv2.circle(img, (int(x), int(y)), int(r), (255, 0, 0), thickness=2)
        elif self._bbox == NORMAL_CONTOUR:
            img = cv2.drawContours(img, cnts, -1, (255, 0, 0), thickness=2)

        return img


class EqualizeItem(MyItem):
    def __init__(self, parent=None):
        super().__init__(' 均衡化 ', parent=parent)
        self._blue = True
        self._green = True
        self._red = True

    def __call__(self, img):
        b, g, r = cv2.split(img)
        if self._blue:
            b = cv2.equalizeHist(b)
        if self._green:
            g = cv2.equalizeHist(g)
        if self._red:
            r = cv2.equalizeHist(r)
        return cv2.merge((b, g, r))


class HoughLineItem(MyItem):
    def __init__(self, parent=None):
        super(HoughLineItem, self).__init__('直线检测', parent=parent)
        self._rho = 1
        self._theta = np.pi / 180
        self._thresh = 10
        self._min_length = 20
        self._max_gap = 5

    def __call__(self, img):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        lines = cv2.HoughLinesP(img, self._rho, self._theta, self._thresh, minLineLength=self._min_length,
                                maxLineGap=self._max_gap)
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        if lines is None: return img
        for line in lines:
            for x1, y1, x2, y2 in line:
                img = cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), thickness=2)
        return img


class LightItem(MyItem):
    def __init__(self, parent=None):
        super(LightItem, self).__init__('亮度调节', parent=parent)
        self._alpha = 1
        self._beta = 0

    def __call__(self, img):
        blank = np.zeros(img.shape, img.dtype)
        img = cv2.addWeighted(img, self._alpha, blank, 1 - self._alpha, self._beta)
        return img


class GammaItem(MyItem):
    def __init__(self, parent=None):
        super(GammaItem, self).__init__('伽马校正', parent=parent)
        self._gamma = 1

    def __call__(self, img):
        gamma_table = [np.power(x / 255.0, self._gamma) * 255.0 for x in range(256)]
        gamma_table = np.round(np.array(gamma_table)).astype(np.uint8)
        return cv2.LUT(img, gamma_table)

class CameraLink(MyItem):
    def __init__(self, parent=None):
        super(CameraLink, self).__init__('相机连接', parent=parent)

    def __call__(self, img):

        return  img

class TakePhotoItem(MyItem):
    def __init__(self, parent=None):
        super(TakePhotoItem, self).__init__('相机拍照', parent=parent)


        # # 引入照相机
        # self.cc = Camera()
        # self.cc.activatecamera(0)

        # self.video_display()

    """

    选择照相机显示

    """

    def video_display(self):
        # 判断照相机是否可用

        # 开 摄像机 线程
        self.display()



        # 使用 照相机

        # 显示 在主界面上

        pass


    def display(self):
        self.h_thread_handle = threading.Thread(target=self.cc.Work_thread, args=(self,))
        self.h_thread_handle.start()


    def __call__(self, img):
        # 连接照相机
        # self.display()

        return  img

    # def show_thread(self):
    #     stFrameInfo = MV_FRAME_OUT_INFO_EX()
    #     img_buff = None
    #     while True:
    #         ret = self.cam.MV_CC_GetOneFrameTimeout(byref(self.buf_cache), self.n_payload_size, stFrameInfo, 1000)
    #         if ret == 0:
    #             # 获取到图像的时间开始节点获取到图像的时间开始节点
    #             self.st_frame_info = stFrameInfo
    #             # print("get one frame: Width[%d], Height[%d], nFrameNum[%d]" % (
    #             # self.st_frame_info.nWidth, self.st_frame_info.nHeight, self.st_frame_info.nFrameNum))
    #             self.n_save_image_size = self.st_frame_info.nWidth * self.st_frame_info.nHeight * 3 + 2048

    #             if img_buff is None:
    #                 img_buff = (c_ubyte * self.n_save_image_size)()

    #             if True == self.b_save_jpg:
    #                 self.Save_jpg()  # ch:保存Jpg图片 | en:Save Jpg
    #             if self.buf_save_image is None:
    #                 self.buf_save_image = (c_ubyte * self.n_save_image_size)()

    #             stParam = MV_SAVE_IMAGE_PARAM_EX()
    #             stParam.enImageType = MV_Image_Bmp;  # ch:需要保存的图像类型 | en:Image format to save
    #             stParam.enPixelType = self.st_frame_info.enPixelType  # ch:相机对应的像素格式 | en:Camera pixel type
    #             stParam.nWidth = self.st_frame_info.nWidth  # ch:相机对应的宽 | en:Width
    #             stParam.nHeight = self.st_frame_info.nHeight  # ch:相机对应的高 | en:Height
    #             stParam.nDataLen = self.st_frame_info.nFrameLen
    #             stParam.pData = cast(self.buf_cache, POINTER(c_ubyte))
    #             stParam.pImageBuffer = cast(byref(self.buf_save_image), POINTER(c_ubyte))
    #             stParam.nBufferSize = self.n_save_image_size  # ch:存储节点的大小 | en:Buffer node size
    #             stParam.nJpgQuality = 80  # ch:jpg编码，仅在保存Jpg图像时有效。保存BMP时SDK内忽略该参数
    #             if True == self.b_save_bmp:
    #                 self.Save_Bmp()  # ch:保存Bmp图片 | en:Save Bmp
    #         else:
    #             continue

    #         # 转换像素结构体赋值
    #         stConvertParam = MV_CC_PIXEL_CONVERT_PARAM()
    #         memset(byref(stConvertParam), 0, sizeof(stConvertParam))
    #         stConvertParam.nWidth = self.st_frame_info.nWidth
    #         stConvertParam.nHeight = self.st_frame_info.nHeight
    #         stConvertParam.pSrcData = self.buf_cache
    #         stConvertParam.nSrcDataLen = self.st_frame_info.nFrameLen
    #         stConvertParam.enSrcPixelType = self.st_frame_info.enPixelType

    #         # Mono8直接显示
    #         if PixelType_Gvsp_Mono8 == self.st_frame_info.enPixelType:
    #             numArray = Mono_numpy(self.buf_cache, self.st_frame_info.nWidth,
    #                                                   self.st_frame_info.nHeight)

    #         # RGB直接显示
    #         elif PixelType_Gvsp_RGB8_Packed == self.st_frame_info.enPixelType:
    #             numArray = Color_numpy(self.buf_cache, self.st_frame_info.nWidth,
    #                                                    self.st_frame_info.nHeight)

    #         # 如果是黑白且非Mono8则转为Mono8
    #         elif True == Is_mono_data(self.st_frame_info.enPixelType):
    #             nConvertSize = self.st_frame_info.nWidth * self.st_frame_info.nHeight
    #             stConvertParam.enDstPixelType = PixelType_Gvsp_Mono8
    #             stConvertParam.pDstBuffer = (c_ubyte * nConvertSize)()
    #             stConvertParam.nDstBufferSize = nConvertSize
    #             ret = self.cam.MV_CC_ConvertPixelType(stConvertParam)
    #             if ret != 0:
    #                 print('show error', 'convert pixel fail! ret = ' + self.To_hex_str(ret))
    #                 continue
    #             cdll.msvcrt.memcpy(byref(img_buff), stConvertParam.pDstBuffer, nConvertSize)
    #             numArray = Mono_numpy(self, img_buff, self.st_frame_info.nWidth,
    #                                                   self.st_frame_info.nHeight)

    #         # 如果是彩色且非RGB则转为RGB后显示
    #         elif True == Is_color_data(self.st_frame_info.enPixelType):
    #             nConvertSize = self.st_frame_info.nWidth * self.st_frame_info.nHeight * 3
    #             stConvertParam.enDstPixelType = PixelType_Gvsp_RGB8_Packed
    #             stConvertParam.pDstBuffer = (c_ubyte * nConvertSize)()
    #             stConvertParam.nDstBufferSize = nConvertSize
    #             ret = self.cam.MV_CC_ConvertPixelType(stConvertParam)
    #             if ret != 0:
    #                 print('show error', 'convert pixel fail! ret = ' + self.To_hex_str(ret))
    #                 continue
    #             cdll.msvcrt.memcpy(byref(img_buff), stConvertParam.pDstBuffer, nConvertSize)
    #             numArray = Color_numpy(img_buff, self.st_frame_info.nWidth,
    #                                                    self.st_frame_info.nHeight)
    #         return numArray

