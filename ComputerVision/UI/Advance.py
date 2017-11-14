from .Basic import Basic

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMessageBox

from ..CV import ImgBase


class Advance(Basic):
    def __init__(self, *args):
        super(Advance, self).__init__(*args)
        self.gray = False
        self.blur = False
        self.gamma = False
        self.usageInfo = """
    README FIRST:
    Two windows will show up, one for input and one for output.
    At first, in input window, draw a rectangle around the object using mouse right button.
    Then press 'n' to segment the object (once or a few times)
    For any finer touch-ups, you can press any of the keys below and draw lines on the areas you want.
    Then again press 'n' for updating the output.
    Key '1' - To select areas of sure background
    Key '2' - To select areas of sure foreground
    Key '3' - To select areas of probable background
    Key '4' - To select areas of probable foreground
    Key 'n' - To update the segmentation
    Key 'r' - To reset the setup
    Key 's' - To save the results
    Key 'o' - To output the processed image
"""

    def controlButtons(self):
        self.showHboxLayout.addWidget(self.grayCheckBox)
        self.grayCheckBox.stateChanged.connect(self.grayStateChange)

        self.showHboxLayout.addWidget(self.blurCheckBox)
        self.blurCheckBox.stateChanged.connect(self.blurStateChange)

        self.showHboxLayout.addWidget(self.gammaCheckBox)
        self.gammaCheckBox.stateChanged.connect(self.gammaStateChange)

        self.showHboxLayout.addWidget(self.showPushButton)
        self.showPushButton.clicked.connect(self.showButtonClick)

    def controlAdvanceButtons(self):
        self.advanceShowHboxLayout.addWidget(self.histPushButton)
        self.histPushButton.clicked.connect(self.histButtonClick)

        self.advanceShowHboxLayout.addWidget(self.grabcutPushButton)
        self.grabcutPushButton.clicked.connect(self.grabcutButtonClick)

    def grayStateChange(self, state):
        if state == Qt.Checked:
            self.gray = True
        else:
            self.gray = False

    def blurStateChange(self, state):
        if state == Qt.Checked:
            self.blur = True
        else:
            self.blur = False

    def gammaStateChange(self, state):
        if state == Qt.Checked:
            self.gamma = True
        else:
            self.gamma = False

    def showButtonClick(self):
        img = ImgBase(self.imgPath)
        if self.gray:
            img.gray()
        if self.blur:
            img.blur()
        if self.gamma:
            img.gamma()
        img.show()

    def histButtonClick(self):
        img = ImgBase(self.imgPath)
        if self.gray:
            img.gray()
        if self.blur:
            img.blur()
        if self.gamma:
            img.gamma()
        img.hist()

    def grabcutButtonClick(self):
        img = ImgBase(self.imgPath)
        if self.gray:
            reply = QMessageBox.warning(self,
                                        "Warning",
                                        "gray-scale image is not allowed",
                                        QMessageBox.Yes | QMessageBox.No)
            return 0
        if self.blur:
            img.blur()
        if self.gamma:
            img.gamma()
        reply = QMessageBox.information(self,
                                        "Usage",
                                        self.usageInfo,
                                        QMessageBox.Yes | QMessageBox.No)
        img.grabcut()
        img.show()
