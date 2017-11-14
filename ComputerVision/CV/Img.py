import numpy as np
from cv2 import imread
from cv2 import namedWindow
from cv2 import imshow
from cv2 import waitKey
from cv2 import cvtColor
from cv2 import COLOR_BGR2GRAY
from cv2 import GaussianBlur
from cv2 import LUT
from cv2 import calcHist
from cv2 import grabCut
from cv2 import GC_INIT_WITH_RECT
from cv2 import error
from cv2 import resize
from cv2 import INTER_CUBIC
from cv2 import findContours
from cv2 import RETR_EXTERNAL
from cv2 import CHAIN_APPROX_NONE
from cv2 import contourArea
from cv2 import minAreaRect
from cv2 import boxPoints
from cv2 import drawContours

import matplotlib.pyplot as plt

from .Grabcut import Grabcut


class ImgBase(object):
    def __init__(self, imgpath=None):
        if not imgpath:
            raise IOError('Invalid imgpath')
        else:
            img = imread(imgpath)
            if type(img) is not np.ndarray:
                raise IOError('Invalid imgpath')
            else:
                self.img = img
                self.imgpath = imgpath
                self.resize()

    # 调整图像
    def resize(self):
        w, h, _ = self.img.shape
        self.img = resize(self.img, (400, int(400 / h * w)),
                          interpolation=INTER_CUBIC)

    # 显示图像
    def show(self, windowname=None):
        if not windowname:
            windowname = 'img'
        namedWindow(windowname)
        imshow(windowname, self.img)
        waitKey(0)

    # 灰度图
    def gray(self):
        self.img = cvtColor(self.img, COLOR_BGR2GRAY)

    # 高斯滤波
    def blur(self):
        self.img = GaussianBlur(self.img, (5, 5), 2)

    # Gamma矫正函数
    def gamma_trans(self, img, gamma):
        gamma_table = [np.power(x / 255.0, gamma) * 255.0 for x in range(256)]
        gamma_table = np.round(np.array(gamma_table)).astype(np.uint8)

        return LUT(img, gamma_table)

    # gamma
    def gamma(self):
        self.img = self.gamma_trans(self.img, 0.5)

    # hist
    def hist(self):
        if len(self.img.shape) == 2:
            self.hist = calcHist([self.img], [0], None, [256], [0.0, 255.0])
            plt.plot(np.arange(256), self.hist)
            plt.show()
        elif len(self.img.shape) == 3:
            self.hist_b = calcHist([self.img], [0], None, [256], [0.0, 255.0])
            self.hist_g = calcHist([self.img], [1], None, [256], [0.0, 255.0])
            self.hist_r = calcHist([self.img], [2], None, [256], [0.0, 255.0])
            plt.plot(np.arange(256), self.hist_b)
            plt.plot(np.arange(256), self.hist_g)
            plt.plot(np.arange(256), self.hist_r)
            plt.show()

    # grabcut
    """
    def grabcut(self):
        if len(self.img.shape) == 2:
            return True
        elif len(self.img.shape) == 3:
            h, w = self.img.shape[:2]
            mask = np.zeros((h, w), np.uint8)
            bgdModel = np.zeros((1, 13 * 5), np.float64)
            fgdModel = np.zeros((1, 13 * 5), np.float64)
            rect = (0, 0, h, w)
            try:
                grabCut(self.img, mask, rect, bgdModel, fgdModel, 5, GC_INIT_WITH_RECT)
            except error as err:
                return True
            else:
                fgMask = np.uint8(np.where((mask == 0) | (mask == 2), 0, 1))
                self.img = self.img * fgMask[:, :, np.newaxis]
                return False
    """

    # grabcut
    def grabcut(self):
        grabcut = Grabcut()
        self.img = grabcut.process(self.imgpath)
        self.crop()

    # 剪切图像
    def crop(self):
        self.mask = np.uint8(np.where((self.img == 0), 0, 255))
        self.mask = cvtColor(self.mask, COLOR_BGR2GRAY)
        namedWindow('crop')
        imshow('crop', self.mask)
        waitKey(0)
        (_, cnts, _) = findContours(
            self.mask, RETR_EXTERNAL, CHAIN_APPROX_NONE)
        c = sorted(cnts, key=contourArea, reverse=True)[0]
        rect = minAreaRect(c)
        box = np.int0(boxPoints(rect))
        drawContours(self.img.copy(), [box], -1, (0, 255, 0), 3)
        (y1, x1, height, width) = self.cropregion(box)
        self.img = self.img[y1: y1 + height, x1: x1 + width]

    def cropregion(self, box):
        Xs = [i[0] for i in box]
        Ys = [i[1] for i in box]
        x1 = min(Xs)
        x2 = max(Xs)
        y1 = min(Ys)
        y2 = max(Ys)
        height = y2 - y1
        width = x2 - x1
        return (y1, x1, height, width)
