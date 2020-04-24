#!/usr/bin/python3
# -*- coding: utf8 -*-
import tkinter as tk
import os
import sys

#DDでファイル名取得　　　
dpath = os.path.dirname(sys.argv[1])
sys.stderr.write(dpath+"\n")

#フォルダを新規作成する
def copyFileTree():
    #ドラッグアンドドロップされたファイルがある階層に新規フォルダ作成
    dirName = dpath+"/exetest/aaa"
    #フォルダが既存かの確認
    if os.path.exists(dirName)==1:
        sys.stderr.write("Error : Directory already Existed !"+"\n") #既存ならエラーコメント
    else:
        os.makedirs(dirName) #なければ新規作成


#ボタンラベル変更
def pushed(b):
 b["text"] = "押されたよ"


#rootウィンドウを作成
root = tk.Tk()
#rootウィンドウのタイトルを変える
root.title("DirTreeCopy")
#rootウィンドウの大きさを320x240に
root.geometry("320x240")

#Label部品を作る
label = tk.Label(root, text="フォルダを新規作成します")
#表示する
label.grid()

#ボタンを作る
button = tk.Button(root, text="フォルダ作成", command= lambda : copyFileTree())
#表示
button.grid()

#メインループ
root.mainloop()
