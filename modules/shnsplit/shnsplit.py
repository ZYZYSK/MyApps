import tkinter as tk
from tkinter import ttk
import json
import os
import sys
import logging
import signal
import subprocess
from tkinter import filedialog
from tkinter.constants import ANCHOR, LEFT
from tkinter import messagebox
import platform

from ..functions import exit_program_tk,handler_sigint_tk

# ログ出力の無効化
# logging.disable(logging.CRITICAL)
# ログ出力設定
logging.basicConfig(level=logging.WARNING, format='%(levelname)s: %(message)s')

def shnsplit():
    logging.basicConfig(level=logging.WARNING,format='%(levelname)s: %(message)s')
    # SIGINTシグナルを受け取る
    signal.signal(signal.SIGINT, handler_sigint_tk)
    #設定情報の取得
    ShnSplit.get_settings()
    #画面表示
    win=tk.Tk()
    app=ShnSplit(master=win)
    app.mainloop()

class ShnSplit(ttk.Frame):
    #設定ファイルへのパス
    settings_path=os.path.join(os.path.dirname(__file__),"shnsplit_settings.json")
    #設定情報
    settings=None
    @classmethod
    def get_settings(cls):#設定情報の取得
        # 設定ファイルを読み込む
        try:
            with open(cls.settings_path, mode='r', encoding="utf-8") as f:
                cls.settings = json.load(f)

        # 設定ファイルが存在しない場合
        except FileNotFoundError:
            exit_program_tk("エラー", "設定ファイル\"{0}\"が見つかりません".format(cls.settings_path))

        # ファイルオープンエラー
        except Exception as e:
            exit_program_tk("エラー", "{0}\n{1}".format(e, sys.exc_info()))


    def __init__(self,master=None):
        #初期設定
        super().__init__(master)
        self.pack()
        #ルートウィンドウの設定
        master.title("shnsplits")
        master.geometry("800x400")
        master.minsize(800,400)
        logging.warning(self.settings)
        #スタイル設定
        self.btn_style=ttk.Style()
        self.btn_style.configure('BtnFontSize.TButton',font=('Yu Gothic',20),anchor="w")
        #種類の指定
        self.frame1=ttk.Frame(master,padding=10)
        self.frame1.pack(expand=0,fill=tk.NONE,anchor=tk.W)
        #種類の指定: ラベル
        self.type_label=ttk.Label(master=self.frame1,style="BtnFontSize.TButton",text="変換先フォーマット: ",justify=LEFT)
        self.type_label.pack(expand=0,fill=tk.NONE,side=tk.LEFT)
        #種類の指定: セレクトボックス
        self.type_list=["wav","aiff","flac","ape","alac"]
        self.type_select=ttk.Combobox(master=self.frame1,style="BtnFontSize.TButton",justify=LEFT,values=self.type_list,font=('Yu Gothic',20))
        if self.settings["default_type"] in self.type_list:
            self.type_select.set(self.settings["default_type"])
        self.type_select.pack(expand=0,fill=tk.NONE,side=tk.LEFT)
        #cueファイル
        self.frame2=ttk.Frame(master,padding=10)
        self.frame2.pack(expand=0,fill=tk.NONE,anchor=tk.W)
        #cueファイル: ラベル
        self.cue_label=ttk.Label(master=self.frame2,style="BtnFontSize.TButton",text="cueファイル: ",justify=LEFT)
        self.cue_label.pack(expand=0,fill=tk.NONE,side=tk.LEFT)
        #cueファイル: エントリー
        self.cue=tk.StringVar()
        self.cue_entry=ttk.Entry(master=self.frame2,justify=LEFT,style="BtnFontSize.TButton",textvariable=self.cue,font=('Yu Gothic',20))
        self.cue_entry.pack(expand=0,fill=tk.NONE,side=tk.LEFT)
        #cueファイル: ボタン
        self.cue_btn=ttk.Button(master=self.frame2,style="BtnFontSize.TButton",text="...")
        self.cue_btn.pack(expand=0,fill=tk.NONE,side=tk.LEFT)
        #flacファイル
        self.frame3=ttk.Frame(master,padding=10)
        self.frame3.pack(expand=0,fill=tk.NONE,anchor=tk.W)
        #flacファイル: ラベル
        self.flac_label=ttk.Label(master=self.frame3,style="BtnFontSize.TButton",text="対象ファイル: ",justify=LEFT)
        self.flac_label.pack(expand=0,fill=tk.NONE,side=tk.LEFT)
        #flacファイル: エントリー
        self.flac=tk.StringVar()
        self.flac_entry=ttk.Entry(master=self.frame3,justify=LEFT,style="BtnFontSize.TButton",textvariable=self.flac,font=('Yu Gothic',20))
        self.flac_entry.pack(expand=0,fill=tk.NONE,side=tk.LEFT)
        #flacファイル: ボタン
        self.flac_btn=ttk.Button(master=self.frame3,style="BtnFontSize.TButton",text="...")
        self.flac_btn.pack(expand=0,fill=tk.NONE,side=tk.LEFT)
        #保存先
        self.frame4=ttk.Frame(master,padding=10)
        self.frame4.pack(expand=0,fill=tk.NONE,anchor=tk.W)
        #保存先: ラベル
        self.dest_label=ttk.Label(master=self.frame4,style="BtnFontSize.TButton",text="保存先: ",justify=LEFT)
        self.dest_label.pack(expand=0,fill=tk.NONE,side=tk.LEFT)
        #保存先: エントリー
        self.dest=tk.StringVar()
        self.dest.set(self.settings["default_path"])
        self.dest_entry=ttk.Entry(master=self.frame4,justify=LEFT,style="BtnFontSize.TButton",textvariable=self.dest,font=('Yu Gothic',20))
        self.dest_entry.pack(expand=0,fill=tk.NONE,side=tk.LEFT)
        #保存先: ボタン
        self.dest_btn=ttk.Button(master=self.frame4,style="BtnFontSize.TButton",text="...")
        self.dest_btn.pack(expand=0,fill=tk.NONE,side=tk.LEFT)
        #変換
        self.convert=ttk.Button(master=self.master,style="BtnFontSize.TButton",text="変換")
        self.convert.pack(expand=0,fill=tk.NONE,anchor=tk.W,padx=10,pady=10)
        #ボタン設定
        self.cue_btn.bind(sequence="<ButtonRelease-1>",func=self.set_cue)
        self.flac_btn.bind(sequence="<ButtonRelease-1>",func=self.set_flac)
        self.dest_btn.bind(sequence="<ButtonRelease-1>",func=self.set_dest)
        self.convert.bind(sequence="<ButtonRelease-1>",func=self.exec_convert)
        self.convert.config(state="disable")
    def set_cue(self,event):
        initialdir="/"
        if os.path.isdir(self.dest.get()):
            initialdir=self.dest.get()
        if self.flac.get()!="":
            initialdir=os.path.dirname(self.flac.get())
        filename=filedialog.askopenfilename(initialdir=initialdir,filetypes=[("cue","*.cue")])
        self.cue.set(filename)
        if filename!="" and self.flac.get()!="":
            self.convert.config(state="enable")
    def set_flac(self,event):
        initialdir="/"
        if os.path.isdir(self.dest.get()):
            initialdir=self.dest.get()
        if self.cue.get()!="":
            initialdir=os.path.dirname(self.cue.get())
        filename=filedialog.askopenfilename(initialdir=initialdir,filetypes=[(i,f"*.{i}") for i in self.type_list])
        self.flac.set(filename)
        if filename!="" and self.cue.get()!="":
            self.convert.config(state="enable")

    def set_dest(self,event):
        initialdir="/"
        if os.path.isdir(self.dest.get()):
            initialdir=self.dest.get()
        if self.cue.get()!="":
            initialdir=os.path.dirname(self.cue.get())
        if self.flac.get()!="":
            initialdir=os.path.dirname(self.flac.get())
        self.dest.set(str(filedialog.askdirectory(initialdir=initialdir)))
    def exec_convert(self,event):
        if str(self.convert["state"])=="disable":
            return
        os.chdir(self.dest.get())
        cmd=None
        if platform.system()=="Linux":
            cmd=f"/usr/bin/shnsplit \"{self.flac.get()}\" -f \"{self.cue.get()}\" -o {self.type_select.get()} -t \"%n %t\""
        logging.warning(os.getcwd())
        logging.warning(cmd)
        try:
            subprocess.run(cmd,shell=True,check=True)
        except subprocess.CalledProcessError:
            messagebox.showerror("エラー","変換に失敗しました．原因として以下が考えられます．\n・shntoolsがインストールされていない\n・保存先が正しくない")
        except Exception as e:
            messagebox.showerror("エラー",e)
        else:
            messagebox.showinfo("メッセージ","変換に成功しました")
    