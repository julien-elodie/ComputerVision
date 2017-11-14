import numpy as np

from cv2 import EVENT_RBUTTONDOWN
from cv2 import EVENT_MOUSEMOVE
from cv2 import rectangle
from cv2 import EVENT_RBUTTONUP
from cv2 import EVENT_LBUTTONDOWN
from cv2 import circle
from cv2 import EVENT_LBUTTONUP
from cv2 import imread
from cv2 import namedWindow
from cv2 import setMouseCallback
from cv2 import moveWindow
from cv2 import imshow
from cv2 import waitKey
from cv2 import imwrite
from cv2 import grabCut
from cv2 import GC_INIT_WITH_RECT
from cv2 import GC_INIT_WITH_MASK
from cv2 import resize
from cv2 import INTER_CUBIC
from cv2 import bitwise_and
from cv2 import destroyAllWindows


class Grabcut(object):
    def __init__(self):
        self.OUTPUT = False

        self.BLUE = [255, 0, 0]        # rectangle color
        self.RED = [0, 0, 255]         # PR BG
        self.GREEN = [0, 255, 0]       # PR FG
        self.BLACK = [0, 0, 0]         # sure BG
        self.WHITE = [255, 255, 255]   # sure FG

        self.DRAW_BG = {'color': self.BLACK, 'val': 0}
        self.DRAW_FG = {'color': self.WHITE, 'val': 1}
        self.DRAW_PR_FG = {'color': self.GREEN, 'val': 3}
        self.DRAW_PR_BG = {'color': self.RED, 'val': 2}

        # setting up flags
        self.rect = (0, 0, 1, 1)
        self.drawing = False         # flag for drawing curves
        self.rectangle = False       # flag for drawing rect
        self.rect_over = False       # flag to check if rect drawn
        self.rect_or_mask = 100      # flag for selecting rect or mask mode
        self.value = self.DRAW_FG    # drawing initialized to FG
        self.thickness = 3           # brush thickness

    def onmouse(self, event, x, y, flags, param):
        # Draw Rectangle
        if event == EVENT_RBUTTONDOWN:
            self.rectangle = True
            self.ix, self.iy = x, y

        elif event == EVENT_MOUSEMOVE:

            if self.rectangle == True:
                self.img = self.copy.copy()
                rectangle(self.img, (self.ix, self.iy), (x, y), self.BLUE, 2)
                self.rect = (min(self.ix, x), min(self.iy, y),
                        abs(self.ix - x), abs(self.iy - y))
                self.rect_or_mask = 0

        elif event == EVENT_RBUTTONUP:
            self.rectangle = False
            self.rect_over = True
            rectangle(self.img, (self.ix, self.iy), (x, y), self.BLUE, 2)
            self.rect = (min(self.ix, x), min(self.iy, y),
                    abs(self.ix - x), abs(self.iy - y))
            self.rect_or_mask = 0
            print(" Now press the key 'n' a few times until no further change \n")

        # draw touchup curves

        if event == EVENT_LBUTTONDOWN:
            if self.rect_over == False:
                print("first draw rectangle \n")
            else:
                self.drawing = True
                circle(self.img, (x, y), self.thickness,
                       self.value['color'], -1)
                circle(self.mask, (x, y), self.thickness,
                       self.value['val'], -1)

        elif event == EVENT_MOUSEMOVE:
            if self.drawing == True:
                circle(self.img, (x, y), self.thickness,
                       self.value['color'], -1)
                circle(self.mask, (x, y), self.thickness,
                       self.value['val'], -1)

        elif event == EVENT_LBUTTONUP:
            if self.drawing == True:
                self.drawing = False
                circle(self.img, (x, y), self.thickness,
                       self.value['color'], -1)
                circle(self.mask, (x, y), self.thickness,
                       self.value['val'], -1)

    def process(self, imgpath):
        self.img = imread(imgpath)
        # resize image
        w, h, _ = self.img.shape
        self.img = resize(self.img,(400, int(400/h*w)),interpolation=INTER_CUBIC)
        # a copy of original image
        self.copy = self.img.copy()
        # mask initialized to PR_BG
        self.mask = np.zeros(self.img.shape[:2], dtype=np.uint8)
        # output image to be shown
        self.output = np.zeros(self.img.shape, np.uint8)

        # input and output windows
        namedWindow('output')
        namedWindow('input')
        setMouseCallback('input', self.onmouse)
        moveWindow('input', self.img.shape[1] + 10, 90)

        print(" Instructions: \n")
        print(" Draw a rectangle around the object using right mouse button \n")

        while(1):

            imshow('output', self.output)
            imshow('input', self.img)
            k = waitKey(1)

            # key bindings
            if k == 27:         # esc to exit
                break
            elif k == ord('1'):  # BG drawing
                print(" mark background regions with left mouse button \n")
                self.value = self.DRAW_BG
            elif k == ord('2'):  # FG drawing
                print(" mark foreground regions with left mouse button \n")
                self.value = self.DRAW_FG
            elif k == ord('3'):  # PR_BG drawing
                self.value = self.DRAW_PR_BG
            elif k == ord('4'):  # PR_FG drawing
                self.value = self.DRAW_PR_FG
            elif k == ord('s'):  # save image
                bar = np.zeros((self.img.shape[0], 5, 3), np.uint8)
                res = np.hstack((self.copy, bar, self.img, bar, self.output))
                outputpath = '/'.join(imgpath.split('/')[:-1]) + '/grabcut_output.png' 
                imwrite(outputpath, res)
                print(" Result saved as image \n")
            elif k == ord('r'):  # reset everything
                print("resetting \n")
                self.rect = (0, 0, 1, 1)
                self.drawing = False
                self.rectangle = False
                self.rect_or_mask = 100
                self.rect_over = False
                self.value = self.DRAW_FG
                self.img = self.copy.copy()
                # mask initialized to PR_BG
                self.mask = np.zeros(self.img.shape[:2], dtype=np.uint8)
                # output image to be shown
                self.output = np.zeros(self.img.shape, np.uint8)
            elif k == ord('n'):  # segment the image
                print(""" For finer touchups, mark foreground and background after pressing keys 0-3
                    and again press 'n' \n""")
                if (self.rect_or_mask == 0): 
                    # grabcut with rect
                    bgdmodel = np.zeros((1, 65), np.float64)
                    fgdmodel = np.zeros((1, 65), np.float64)
                    grabCut(self.copy, self.mask, self.rect,
                            bgdmodel, fgdmodel, 5, GC_INIT_WITH_RECT)
                    self.rect_or_mask = 1
                elif self.rect_or_mask == 1:         # grabcut with mask
                    bgdmodel = np.zeros((1, 65), np.float64)
                    fgdmodel = np.zeros((1, 65), np.float64)
                    grabCut(self.copy, self.mask, self.rect,
                            bgdmodel, fgdmodel, 5, GC_INIT_WITH_MASK)
            elif k == ord('o'):  # output image
                self.OUTPUT = True
                break

            self.fgMask = np.where(
                (self.mask == 0) | (self.mask == 2), 0, 255).astype('uint8')
            self.output = bitwise_and(self.copy, self.copy, mask=self.fgMask)

        destroyAllWindows()
        if self.OUTPUT:
            print(" Output the processed image \n")
            return self.output
