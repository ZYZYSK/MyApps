import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import subprocess
import os
import sys
import signal
import json

from ..functions import exit_program_tk, handler_sigint_tk


def pc_manager():
    # SIGINTシグナルを受け取る
    signal.signal(signal.SIGINT, handler_sigint_tk)
    # リストを読み込む
    PCManager.get_list()
    # 画面表示
    win = tk.Tk()
    app = PCManager(master=win)
    app.mainloop()


class PCManager(ttk.Frame):
    # リストファイルのパス
    list_path = os.path.join(os.path.dirname(__file__), "list.json")
    # リスト
    list_data = None
    # アイコンへのパス: app.ico
    icn_app = os.path.join(os.path.dirname(__file__), 'app.ico')

    @classmethod
    def get_list(cls):  # リストの取得
        # 設定ファイルを読み込む
        try:
            with open(cls.list_path, mode='r', encoding="utf-8") as f:
                cls.list_data = json.load(f)

        # 設定ファイルが存在しない場合
        except FileNotFoundError:
            exit_program_tk("エラー", "設定ファイル\"{0}\"が見つかりません".format(cls.list_path))

        # ファイルオープンエラー
        except Exception as e:
            exit_program_tk("エラー", "{0}\n{1}".format(e, sys.exc_info()))

    def __init__(self, master=None) -> None:
        super().__init__(master)
        self.pack()
        self.master = master
        # ルートウィンドウの設定: タイトルバーの名前
        master.title('PC Manager')
        #ルートウィンドウの設定: ウィンドウサイズ変更禁止
        master.resizable(0, 0)
        # ルートウィンドウの設定: アイコン画像
        master.iconbitmap(self.icn_app)
        # 文字の大きさ
        self.btn_style = ttk.Style()
        self.btn_style.configure("BtnStyle.TButton", font=('Yu Gothic', 20))
        # ボタンの動作を指定
        for i in self.list_data:
            btn = ttk.Button(self, text=i, command=self.make_btn(i, self.list_data[i]), style="BtnStyle.TButton")
            btn.pack(anchor=tk.W, side=tk.TOP)

    def make_btn(self, name, command):
        return lambda: self.run(name, command)

    def run(self, name, command):
        print(command)
        subprocess.Popen(command, shell=True)
