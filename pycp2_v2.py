#!/usr/bin/python3
# -*- coding: utf8 -*-
#親フォルダと一緒にファイルコピー
#
# dekapoppo
#
# 20200426 v2.0
#
import os,sys
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import shutil

# フォルダ指定の関数
def dirdialog_clicked():
    iDir = os.path.abspath(os.path.dirname(__file__))
    iDirPath = filedialog.askdirectory(initialdir = iDir)
    entry1.set(iDirPath.replace("/","\\")) #バックスラッシュに変換（windows用）

# ファイル指定の関数
def filedialog_clicked():
    fTyp = [("", "*")]
    iFile = os.path.abspath(os.path.dirname(__file__))
    iFilePath = filedialog.askopenfilename(filetype = fTyp, initialdir = iFile)
    entry2.set(iFilePath.replace("/","\\")) #バックスラッシュに変換（windows用）
    changeNewPath() #コピーの更新

# 実行ボタン押下時の実行関数
def conductMain():
    text = ""
    dirPath = entry1.get()
    filePath = entry2.get()
    newPath = entry3.get()
    if dirPath:
        text += "コピー先　：\n" + dirPath + "\n"
        if filePath:
            if newPath:
                text += "コピー内容：\n" + newPath
                messagebox.showinfo("info", text)
            else:
                messagebox.showinfo("error","「コピー内容」を更新してください")
        else:
            messagebox.showerror("error", "「コピーファイル」のパスを指定してください")
    else:
        messagebox.showerror("error", "「コピー先フォルダ」のパスを指定してください")
    #以下コピー処理
    copyDirAndFile()

#label変更
def changeNewPath():
    #ファイルのフルパス取得
    fpath = entry2.get()
    #print(fpath)
    #↑で指定してる時だけ処理
    if fpath:
        #上に上がるフォルダの階層
        upDirNum = int(sptxt1.get()) #スピンボックスの値を取得
        #------------------------------------------
        dList = fpath.split("\\") #フォルダを文字列で分ける
        #print(dList)
        #print(dList)
        #upDirNumが有効な時だけ処理
        if upDirNum<(len(dList)-1): #ドライブまで含めないように－１
            #上がるフォルダまで含めたパス作成
            newpath = dList[-1]
            for i in range(upDirNum):
                newpath = dList[(i+2)*(-1)]+"\\"+newpath
        else:
            print("Error!  MaxNum = "+str(len(dList)-2))
            newpath = fpath[3:]
        entry3.set(newpath) #新しいパス表示
    else:
        entry3.set("　◆◆◆　エラー　◆◆◆　「コピーファイル」を指定してから、親階層を指定してください")


#フォルダの新規作成
def copyDirAndFile():
    dirPath = entry1.get()
    filePath = entry2.get()
    newPath = entry3.get()
    ##まずフォルダ作成
    #コピー先フォルダ、コピー内容の取得
    newPathParts = newPath.rsplit("\\",1) #右から、1回だけ分割
    #追加するフォルダ
    newPathDir = dirPath +"\\"+ newPathParts[0]
    print(newPathDir)
    #フォルダが既存かの確認
    if os.path.exists(newPathDir)==1:
        sys.stderr.write("Error : Directory already Existed !"+"\n") #既存ならエラーコメント
        messagebox.showerror("error", "Error : Directory already Existed !")
    else:
        os.makedirs(newPathDir) #なければ新規作成
    ##次にファイルコピー
    newPathFull = dirPath + "\\" + newPath
    newPathFull = newPathFull.replace("\\","\\\\") #shutil用にバックスラッシュを２つに
    shutil.copy(filePath,newPathFull)


#--------------------------------------------------------------
if __name__ == "__main__":

    # rootの作成
    root = Tk()
    root.title("親フォルダ含めたファイルコピー")

    # Frame1の作成
    frame1 = ttk.Frame(root, padding=10)
    frame1.grid(row=0, column=1, sticky=E)

    # 「フォルダ参照」ラベルの作成
    IDirLabel = ttk.Label(frame1, text="コピー先フォルダ＞＞", padding=(5, 2))
    IDirLabel.pack(side=LEFT)

    # 「フォルダ参照」エントリーの作成
    entry1 = StringVar()
    IDirEntry = ttk.Entry(frame1, textvariable=entry1, width=100)
    IDirEntry.pack(side=LEFT)

    # 「フォルダ参照」ボタンの作成
    IDirButton = ttk.Button(frame1, text="参照", command=dirdialog_clicked)
    IDirButton.pack(side=LEFT)

    # Frame2の作成
    frame2 = ttk.Frame(root, padding=10)
    frame2.grid(row=2, column=1, sticky=E)

    # 「ファイル参照」ラベルの作成
    IFileLabel = ttk.Label(frame2, text="コピーファイル＞＞", padding=(5, 2))
    IFileLabel.pack(side=LEFT)

    # 「ファイル参照」エントリーの作成
    entry2 = StringVar()
    IFileEntry = ttk.Entry(frame2, textvariable=entry2, width=100)
    IFileEntry.pack(side=LEFT)

    # 「ファイル参照」ボタンの作成
    IFileButton = ttk.Button(frame2, text="参照", command=filedialog_clicked)
    IFileButton.pack(side=LEFT)

    # Frame3の作成
    frame3 = ttk.Frame(root, padding=10)
    frame3.grid(row=5, column=1, sticky=(W,E))

    # 「コピー内容」ラベルの作成
    IFileLabel = ttk.Label(frame3, text="コピー内容＞＞", padding=(5, 2))
    IFileLabel.pack(side=LEFT)

    # ■ スピンボックスの設置
    sptxt1 = StringVar()
    sptxt1.set(1)
    sp1 = ttk.Spinbox(frame3,textvariable=sptxt1,width=10,from_=1,to=99,increment=1,state="readonly",command=changeNewPath)
    sp1.pack(side=RIGHT)

    # 「作成フォルダパス」エントリーの作成
    entry3 = StringVar()
    IFileEntry = ttk.Entry(frame3, textvariable=entry3, width=100,state="readonly")
    IFileEntry.pack(side=RIGHT)

    # Frame4の作成
    frame4 = ttk.Frame(root, padding=10)
    frame4.grid(row=7,column=1,sticky=W)

    # 実行ボタンの設置
    button1 = ttk.Button(frame4, text="実行", command=conductMain)
    button1.pack(fill = "x", padx=30, side = "left")

    # キャンセルボタンの設置
    #button2 = ttk.Button(frame4, text=("閉じる"), command=quit)
    #button2.pack(fill = "x", padx=30, side = "left")

    root.mainloop()
