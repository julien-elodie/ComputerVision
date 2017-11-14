from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QAction
from PyQt5.QtWidgets import qApp
from PyQt5.QtWidgets import QToolBar
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QSplitter
from PyQt5.QtWidgets import QFileSystemModel
from PyQt5.QtCore import QDir
from PyQt5.QtWidgets import QTreeView
from PyQt5.QtWidgets import QHeaderView
# from PyQt5.QtWidgets import QTextEdit
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QCheckBox


class BasicUI(QMainWindow):
    """
    实现窗口界面布局
    """

    def __init__(self, *args):
        super(BasicUI, self).__init__(*args)
        self.initUI()

    def initUI(self):
        self.initAction()
        self.initMenuBar()
        self.initToolBar()
        self.initStatusBar()
        self.initWidget()

    def initAction(self):
        self.exitAction = QAction('&Exit', self)
        self.exitAction.setStatusTip('Exit')

        self.fileAction = QAction('&File', self)
        self.fileAction.setStatusTip('File')

        self.openAction = QAction('&Open', self)
        self.openAction.setStatusTip('Open')

    def initMenuBar(self):
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(self.fileAction)
        exitMenu = menubar.addMenu('&Exit')
        exitMenu.addAction(self.exitAction)

    def initToolBar(self):
        self.toolbar = QToolBar(self)
        self.addToolBar(Qt.LeftToolBarArea, self.toolbar)
        self.toolbar.addAction(self.fileAction)
        self.toolbar.addAction(self.exitAction)

    def initStatusBar(self):
        statusbar = self.statusBar()
        statusbar.showMessage('Ready', 2000)

    def initWidget(self):
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)

        self.centralHboxLayout = QHBoxLayout(self.centralWidget)

        self.initFileWidget()
        self.initImgWidget()

        self.centralHboxLayout.addWidget(self.fileWidget)
        self.centralHboxLayout.addWidget(self.imgWidget)

        self.centralHboxLayout.setStretch(0, 1)
        self.centralHboxLayout.setStretch(1, 2)

    def initFileWidget(self):
        self.fileWidget = QWidget()
        self.fileVboxLayout = QVBoxLayout(self.fileWidget)
        self.fileVboxLayout.setContentsMargins(0, 0, 0, 0)

        self.fileHboxLayout = QHBoxLayout()
        self.lineedit = QLineEdit()
        self.pushbutton = QPushButton()
        self.pushbutton.setText('Browse')
        self.pushbutton.setStatusTip('Browse')
        self.fileHboxLayout.addWidget(self.lineedit)
        self.fileHboxLayout.addWidget(self.pushbutton)

        self.fileVboxLayout.addLayout(self.fileHboxLayout)

        self.initTreeView()

        self.fileVboxLayout.addWidget(self.treeview)

    def initTreeView(self):
        self.filespliter = QSplitter()
        self.filesystemmodel = QFileSystemModel()
        self.dir = QDir()
        self.directory = self.dir.currentPath()
        self.lineedit.setText(self.directory)
        self.filesystemmodel.setRootPath(self.directory)
        self.treeview = QTreeView(self.filespliter)
        self.treeview.setModel(self.filesystemmodel)
        self.treeview.setRootIndex(self.filesystemmodel.index(self.directory))
        self.treeviewheader = self.treeview.header()
        self.treeviewheader.setSectionResizeMode(QHeaderView.ResizeToContents)
        self.treeviewheader.setStretchLastSection(False)

    def initImgWidget(self):
        self.imgWidget = QWidget()
        self.imgVboxLayout = QVBoxLayout(self.imgWidget)
        self.imgVboxLayout.setContentsMargins(0, 0, 0, 0)

        self.imgView = QLabel("add a image file")
        self.imgView.setAlignment(Qt.AlignCenter)
        self.imgVboxLayout.addWidget(self.imgView)

        self.initButtons()
        self.initAdvanceButtons()

    def initButtons(self):
        self.grayCheckBox = QCheckBox()
        self.grayCheckBox.setText('gray')
        self.grayCheckBox.setStatusTip('gray')

        self.blurCheckBox = QCheckBox()
        self.blurCheckBox.setText('blur')
        self.blurCheckBox.setStatusTip('blur')

        self.gammaCheckBox = QCheckBox()
        self.gammaCheckBox.setText('gamma')
        self.gammaCheckBox.setStatusTip('gamma')

        self.showPushButton = QPushButton()
        self.showPushButton.setText('Show')
        self.showPushButton.setStatusTip('Show')

        self.showHboxLayout = QHBoxLayout()
        self.imgVboxLayout.addLayout(self.showHboxLayout)

    def initAdvanceButtons(self):
        self.histPushButton = QPushButton()
        self.histPushButton.setText('Hist')
        self.histPushButton.setStatusTip('Hist')

        self.grabcutPushButton = QPushButton()
        self.grabcutPushButton.setText('Grabcut')
        self.grabcutPushButton.setStatusTip('Grabcut')

        self.advanceShowHboxLayout = QHBoxLayout()
        self.imgVboxLayout.addLayout(self.advanceShowHboxLayout)