# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'pycopyGUI3.ui'
##
## Created by: Qt User Interface Compiler version 5.14.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import (QCoreApplication, QDate, QDateTime, QMetaObject,
    QObject, QPoint, QRect, QSize, QTime, QUrl, Qt)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
    QFontDatabase, QIcon, QKeySequence, QLinearGradient, QPalette, QPainter,
    QPixmap, QRadialGradient)
from PySide2.QtWidgets import *

#カスタムウィじぇえと（サブクラス？）がうまく読み込まれないので追加
#from droppablelineedit import DroppableLineEdit
class DroppableLineEdit(QLineEdit):
    def __init__(self, parent):
        super(DroppableLineEdit, self).__init__(parent)
        self.setDragEnabled(True)

    #Dropだけしか使わなくてもdragEventとdragMoveEventは必要！！！
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls:
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls:
            event.setDropAction(Qt.CopyAction)
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls:
            event.setDropAction(Qt.CopyAction)
            event.accept()
            l = []
            for url in event.mimeData().urls(): #複数ファイル選択時も使える
                l.append(str(url.toLocalFile()))
                #self.emit(SIGNAL("dropped"), l)
            #なぜか末尾にスラッシュ残るときがあるので確認して修正
            if l[0][-1]=="/":
                self.setText(l[0][:-1]) #末尾削除
            else:
                self.setText(l[0])
        else:
            event.ignore()

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(368, 179)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.lineEdit_2 = DroppableLineEdit(self.centralwidget)
        self.lineEdit_2.setObjectName(u"lineEdit_2")
        self.lineEdit_2.setDragEnabled(True)

        self.gridLayout.addWidget(self.lineEdit_2, 1, 1, 1, 1)

        self.lineEdit_3 = QLineEdit(self.centralwidget)
        self.lineEdit_3.setObjectName(u"lineEdit_3")
        self.lineEdit_3.setEnabled(True)
        self.lineEdit_3.setAcceptDrops(True)

        self.gridLayout.addWidget(self.lineEdit_3, 2, 1, 1, 1)

        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)

        self.btn1 = QPushButton(self.centralwidget)
        self.btn1.setObjectName(u"btn1")

        self.gridLayout.addWidget(self.btn1, 0, 2, 1, 1)

        self.btn2 = QPushButton(self.centralwidget)
        self.btn2.setObjectName(u"btn2")

        self.gridLayout.addWidget(self.btn2, 1, 2, 1, 1)

        self.spinBox_1 = QSpinBox(self.centralwidget)
        self.spinBox_1.setObjectName(u"spinBox_1")

        self.gridLayout.addWidget(self.spinBox_1, 2, 2, 1, 1)

        self.lineEdit_1 = DroppableLineEdit(self.centralwidget)
        self.lineEdit_1.setObjectName(u"lineEdit_1")
        self.lineEdit_1.setDragEnabled(True)

        self.gridLayout.addWidget(self.lineEdit_1, 0, 1, 1, 1)

        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)


        self.verticalLayout.addLayout(self.gridLayout)

        self.btnRun = QPushButton(self.centralwidget)
        self.btnRun.setObjectName(u"btnRun")
        self.btnRun.setMinimumSize(QSize(0, 0))

        self.verticalLayout.addWidget(self.btnRun)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 368, 22))
        self.menuHelp = QMenu(self.menubar)
        self.menuHelp.setObjectName(u"menuHelp")
        MainWindow.setMenuBar(self.menubar)

        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Target Dir >>", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Target Dir >>", None))
        self.btn1.setText(QCoreApplication.translate("MainWindow", u"brows", None))
        self.btn2.setText(QCoreApplication.translate("MainWindow", u"brows", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Source File >>", None))
        self.btnRun.setText(QCoreApplication.translate("MainWindow", u"Run", None))
        self.menuHelp.setTitle(QCoreApplication.translate("MainWindow", u"Help", None))
    # retranslateUi
