from .BasicUI import BasicUI

from PyQt5.QtWidgets import QDesktopWidget
from PyQt5.QtWidgets import qApp
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QImage
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt


class Basic(BasicUI):
    """
    实现窗口逻辑
    """

    def __init__(self):
        super(Basic, self).__init__()

        self.controlUI()

    def controlUI(self):
        self.controlAction()
        self.controlMenuBAr()
        self.controlToolBar()
        self.controlStatusBar()
        self.controlWidget()

        self.resize(1024, 600)
        self.moveCentered()

        self.setWindowTitle("Basic")

    def moveCentered(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()

        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def controlAction(self):
        self.exitAction.setShortcut('ctrl+Q')
        # self.exitAction.triggered.connect(qApp.quit)
        self.exitAction.triggered.connect(self.exitActionClick)

        self.fileAction.triggered.connect(self.fileActionClick)

        self.openAction.setShortcut('ctrl+O')
        self.openAction.triggered.connect(self.fileButtonClick)

    def exitActionClick(self):
        self.close()

    def fileActionClick(self):
        if self.fileWidget.isVisible():
            self.fileWidget.hide()
        else:
            self.fileWidget.show()

    def fileButtonClick(self):
        directory = QFileDialog.getExistingDirectory(
            self, 'Select Directory', self.directory)
        if directory:
            self.directory = directory
            self.lineedit.setText(self.directory)
            self.filesystemmodel.setRootPath(self.directory)
            self.treeview.setRootIndex(
                self.filesystemmodel.index(self.directory))

    def controlMenuBAr(self):
        pass

    def controlToolBar(self):
        pass

    def controlStatusBar(self):
        pass

    def controlWidget(self):
        self.controlFileWidget()
        self.controlImgWidget()

    def controlFileWidget(self):
        self.pushbutton.clicked.connect(self.fileButtonClick)
        self.treeview.doubleClicked.connect(self.treeViewItemClick)

    def treeViewItemClick(self):
        index = self.treeview.selectionModel().currentIndex()
        path = self.filesystemmodel.filePath(index)
        if path.split('.')[-1] in ["jpg", "jpeg", "bmp", "png"]:
            # open pic
            self.imgPath = path
            self.img = QImage(self.imgPath)
            self.imgView.setPixmap(
                QPixmap
                .fromImage(self.img)
                .scaled(self.imgView.size(), Qt.KeepAspectRatio,
                        Qt.SmoothTransformation)
            )
            # add button
            self.controlButtons()
            self.controlAdvanceButtons()

    def controlButtons(self):
        pass

    def controlAdvanceButtons(self):
        pass

    def controlImgWidget(self):
        pass

    def closeEvent(self, event):
        reply = QMessageBox.question(
            self,
            'Message',
            'Are you sure to exit?',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
