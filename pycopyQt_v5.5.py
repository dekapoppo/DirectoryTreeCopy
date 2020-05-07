# -*- coding: utf8 -*-
#親フォルダと一緒にファイルコピー
#
# dekapoppo
#
# 20200426 v2.0
# 20200428 v2.1  Windows,Mac 両方のOSに対応
# 20200504 v5.0  Qt for Python(pyside2)で作り直し
# 20200504 v5.3  ファイルのドラッグ&ドロップに対応
#

import os,sys
from PySide2.QtWidgets import QMainWindow,QFileDialog,QApplication,QMessageBox,QLineEdit,QSpinBox
from PySide2.QtGui  import Qt
import shutil

##GUIファイルの読み込み方
#from PySide2.QtUiTools import QUiLoader #.ui
from pycopyGUI3 import Ui_MainWindow #.py

CURRENT_PATH = os.path.dirname(os.path.abspath(sys.argv[0]))

#OSを判別してコネクション文字列を設定
if os.name == 'nt': #windows
    cnct = "\\"
elif os.name == "posix":
    cnct = "/"

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

"""
class CustomQUiLoader(QUiLoader): #カスタムWidgetクラス？作ったらこちらに追加して呼び出し
    def createWidget(self, className, parent=None, name=''):
        if className == 'DroppableLineEdit':
            ret = DroppableLineEdit(parent)
            ret.setObjectName(name)
            return ret
        return super().createWidget(className, parent, name)
"""

class MainUi(QMainWindow):
    def __init__(self, parent=None):
        super(MainUi, self).__init__(parent)
        #Qt Designer で作ったGUIを読み込み
        #.py
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        #.ui
        """
        self.ui = CustomQUiLoader().load(os.path.join(CURRENT_PATH, 'pycopyGUI3.ui'))
        self.setCentralWidget(self.ui)
        self.setAcceptDrops(True)
        """
        # Signal作成
        self.ui.btn1.clicked.connect(self.selectDirectory)
        self.ui.btn2.clicked.connect(self.openFile)
        self.ui.lineEdit_2.textChanged.connect(self.numChange)
        self.ui.spinBox_1.valueChanged.connect(self.numChange)
        self.ui.btnRun.clicked.connect(self.preCheck)
        #self.ui.lineEdit_2.dropEvent("jjj")

    # ディレクトリ選択ダイアログの表示
    def selectDirectory(self):
        dirName = self.ui.lineEdit_1.text() #lineEditの文字列取得してDirNameに代入
        #dirNameの中身があるか確認
        if dirName == "":
            selDir = QFileDialog.getExistingDirectory(self, 'Select Directory', os.path.expanduser('~') + '/Desktop')
        else:
            selDir = QFileDialog.getExistingDirectory(self, 'Select Directory', dirName)
        #Dialogの選択結果を反映
        if selDir != "":
            #QMessageBox.information(self, "Directory", dirName)
            dirName = selDir
            self.ui.lineEdit_1.setText(dirName)

    # ファイルオープンダイアログの表示
    def openFile(self):
        fileName = self.ui.lineEdit_2.text() #lineEditの文字列取得してDirNameに代入
        #dirNameの中身があるか確認
        if fileName == "":
            (selFile, selectedFilter) = QFileDialog.getOpenFileName(self, 'Open file', os.path.expanduser('~') + '/Desktop')
        else:
            (selFile, selectedFilter) = QFileDialog.getOpenFileName(self, 'Open file', fileName)
        #Dialogの選択結果を反映
        if selFile != "":
            #QMessageBox.information(self, "Directory", dirName)
            fileName = selFile
            self.ui.lineEdit_2.setText(fileName)

    # 親階層の変更
    def numChange(self):
        #fpath = self.ui.lineEdit_2.text()
        #self.ui.lineEdit_3.setText(fileName)
        #
        #ファイルのフルパス取得
        fpath = self.ui.lineEdit_2.text().replace("\\","/") #テキストボックス内のパス区切りがバックスラッシュのときは／に置換
        #print(fpath)
        #↑で指定してる時だけ処理
        if fpath:
            #上に上がるフォルダの階層
            upDirNum = self.ui.spinBox_1.value() #スピンボックスの値を取得
            #------------------------------------------
            dList = fpath.split("/") #フォルダを文字列で分ける
            #upDirNumが有効な時だけ処理
            if upDirNum<(len(dList)-1): #ドライブまで含めないように－１
                #上がるフォルダまで含めたパス作成
                newpath = dList[-1]
                for i in range(upDirNum):
                    newpath = dList[(i+2)*(-1)]+"/"+newpath
            else:
                print("Error!  MaxNum = "+str(len(dList)-2))
                if os.name=="nt": #windowsなら
                    newpath = fpath[3:]
                elif os.name=="posix": #macなら
                    newpath = fpath[1:]
            self.ui.lineEdit_3.setText(newpath) #新しいパス表示
        else:
            self.ui.lineEdit_3.setText("Please set 'Source File'")

    # 実行ボタン押下時のプレチェック
    def preCheck(self):
        text = ""
        dirName = self.ui.lineEdit_1.text().replace("\\","/") #テキストボックス内のパス区切りがバックスラッシュのときは／に置換
        fileName = self.ui.lineEdit_2.text().replace("\\","/") #テキストボックス内のパス区切りがバックスラッシュのときは／に置換
        newPath = self.ui.lineEdit_3.text().replace("\\","/") #テキストボックス内のパス区切りがバックスラッシュのときは／に置換
        if dirName:
            text += "Target Dir :\n" + dirName + "\n"
            if fileName:
                if newPath:
                    text += "Copy Info :\n" + newPath
                    ret = QMessageBox.information(self,"info", "Copy File and Directories?\n\n"+text, QMessageBox.Yes, QMessageBox.No)
                    if ret == QMessageBox.Yes:
                        #Yesの時はコピー処理
                        self.copyDirAndFile()
                else:
                    QMessageBox.information(self, "error"," Error: Please change 'Copy File and Dir' Number, before Run !")
            else:
                QMessageBox.information(self, "error"," Error: Please set 'Source File' before Run !")
        else:
            QMessageBox.information(self, "error"," Error: Please set 'Target Dirs' before Run !")

    #フォルダの新規作成
    def copyDirAndFile(self):
        dirName = self.ui.lineEdit_1.text().replace("\\","/") #テキストボックス内のパス区切りがバックスラッシュのときは／に置換
        fileName = self.ui.lineEdit_2.text().replace("\\","/") #テキストボックス内のパス区切りがバックスラッシュのときは／に置換
        newPath = self.ui.lineEdit_3.text().replace("\\","/") #テキストボックス内のパス区切りがバックスラッシュのときは／に置換
        ##まずフォルダ作成
        #コピー先フォルダ、コピー内容の取得
        newPathParts = newPath.rsplit("/",1) #右から、1回だけ分割
        #追加するフォルダ
        newPathDir = dirName +"/"+ newPathParts[0]
        print(newPathDir)
        #フォルダが既存かの確認
        if os.path.exists(newPathDir)==1:
            sys.stderr.write("Error : Directory already Existed !"+"\n") #既存ならエラーコメント
            QMessageBox.information(self, "error", "Error : Directory already Existed !")
        else:
            os.makedirs(newPathDir) #なければ新規作成
        ##次にファイルコピー
        newPathFull = dirName + "/" + newPath
        print(newPathFull)
        if cnct=="\\": #windowsの時
            newPathFull = newPathFull.replace("/","\\\\") #shutil用にバックスラッシュを２つに [windows用]
        shutil.copy(fileName,newPathFull)
        #結果表示
        QMessageBox.information(self, "info", "Copy Successed !")



if __name__ == '__main__':
    app = QApplication(sys.argv)
    myUi = MainUi()
    myUi.show()
    sys.exit(app.exec_())
