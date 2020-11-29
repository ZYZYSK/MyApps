import tkinter as tk
import json
import os
import sys
import logging

# ログ出力の無効化
# logging.disable(logging.CRITICAL)

# 境界線の太さ
BORDER_DEBUG = 10
BORDER_RELEASE = 1


class BaseWindow(tk.Frame):
    # 設定ファイルのパス
    settings_path = os.path.join(os.path.dirname(__file__), "settings.json")
    # 設定情報
    settings = None
    # アイコンへのパス
    img_full_path = os.path.join(os.path.dirname(__file__), 'icons', 'fullscreen.png')
    img_vs_path = os.path.join(os.path.dirname(__file__), 'icons', 'vs.png')
    img_sp_path = os.path.join(os.path.dirname(__file__), 'icons', 'sp.png')
    img_multi_path = os.path.join(os.path.dirname(__file__), 'icons', 'multi.png')

    @staticmethod
    def exitProgram(e, info=None):  # プログラムを終了させる
        if not info is None:
            exc_type, exc_obj, exc_tb = info
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print("{0} {1} {2}行目\n{3}".format(exc_type, fname, exc_tb.tb_lineno, e))
        print("{0}\n\'q\'で終了します".format(e))
        while True:
            s = input()
            if s == 'q':
                sys.exit()

    @classmethod
    def getSettings(cls):  # 設定情報を取得する
        # 設定ファイルを読み込む
        try:
            with open(cls.settings_path, mode='r') as f:
                settings = json.load(f)

        # 設定ファイルが存在しない場合
        except FileNotFoundError:
            ("[エラー] 設定ファイルが見つかりません: {0}".format(cls.settings_path))

        # ファイルオープンエラー
        except Exception as e:
            BaseWindow.exitProgram(e, sys.exc_info())

        else:
            # Debug
            logging.debug(settings)

    def __init__(self, master=None):

        # 初期設定
        super().__init__(master)
        self.pack()
        self.init_start(master)
        # レイヤーの初期化
        self.layer = [Viewer_OneFrame()] * 4
        # 全体画面
        self.frame_base = tk.Frame(master, bd=0, relief='solid')
        self.frame_base.pack(expand=True, fill=tk.BOTH)
        # ツールバー
        self.toolbar = tk.Frame(self.frame_base, bd=1, relief='solid')
        self.toolbar.pack(expand=False, anchor=tk.N, fill=tk.X)
        # ツールバーのボタン(全画面)
        self.img_full = tk.PhotoImage(file=self.img_full_path)
        self.btn_full = tk.Button(self.toolbar, width=self.toolbar_height, image=self.img_full)
        self.btn_full.bind('<1>', self.show_full)
        self.btn_full.grid(row=0, column=0)
        # ツールバーのボタン(縦2画面)
        self.img_vs = tk.PhotoImage(file=self.img_vs_path)
        self.btn_vs = tk.Button(self.toolbar, width=self.toolbar_height, image=self.img_vs)
        self.btn_vs.bind('<1>', self.show_vs)
        self.btn_vs.grid(row=0, column=1)
        # ツールバーのボタン(横2画面)
        self.img_sp = tk.PhotoImage(file=self.img_sp_path)
        self.btn_sp = tk.Button(self.toolbar, width=self.toolbar_height, image=self.img_sp)
        self.btn_sp.grid(row=0, column=2)
        # ツールバーのボタン(4画面)
        self.img_multi = tk.PhotoImage(file=self.img_multi_path)
        self.btn_multi = tk.Button(self.toolbar, width=self.toolbar_height, image=self.img_multi)
        self.btn_multi.grid(row=0, column=3)

    # 起動時の初期設定
    def init_start(self, master):
        # プログラムの解像度
        master.geometry('1920x1080')
        # プログラムタイトル　
        master.title('Weather Viewer')

    def show_full(self, event):  # 全画面表示
        # 画像を表示する画面[フルスクリーン]
        self.frame_full = tk.Frame(self.frame_base, bd=10, relief='solid')
        self.frame_full.pack(expand=True, anchor=tk.N, fill=tk.BOTH)
        # self.show_set(self.frame_full, 0)

    def show_vs(self, event):  # 縦2画面表示
        # 左側の画面
        self.frame_vs1 = tk.Frame(self.frame_base, bd=10, relief='solid')
        self.frame_vs1.pack(expand=True, anchor=tk.W, side=tk.LEFT, fill=tk.BOTH)
        # self.show_set(self.frame_vs1, 0)
        # 右側の画面
        self.frame_vs2 = tk.Frame(self.frame_base, bd=10, relief='solid')
        self.frame_vs2.pack(expand=True, anchor=tk.E, side=tk.LEFT, fill=tk.BOTH)
        # self.show_set(self.frame_vs2, 1)

    def show_set(self, frame_a, n, time=None):  # 1画像につき表示する画面
        # コントロールバー
        self.layer[n].ctrlbar = tk.Frame(frame_a, bd=1, relief='solid')
        self.layer[n].ctrlbar.pack(expand=False, anchor=tk.N, fill=tk.X)
        # コントロールバーのボタン(時間を戻す)
        self.layer[n].btn_timeminus = tk.Button(self.layer[n].ctrlbar, text='<')
        self.layer[n].btn_timeminus.grid(row=0, column=0)
        # コントロールバーのボタン(現在時間)
        text_time = '----/--/--/--:--' if time is None else time.strftime('%Y/%m/%d/%H:%M')
        self.layer[n].btn_time = tk.Button(self.layer[n].ctrlbar, text=text_time)
        self.layer[n].btn_time.grid(row=0, column=1)
        # コントロールバーのボタン(時間を進める)
        self.layer[n].btn_timeplus = tk.Button(self.layer[n].ctrlbar, text='>')
        self.layer[n].btn_timeplus.grid(row=0, column=2)
        # コントロールバーのボタン(画像の種類)
        self.layer[n].map_type = ttk.Combobox(self.layer[n].ctrlbar, textvariable=self.layer[n].map_name, values=self.map_list)
        self.layer[n].map_type.set(self.map_list[0])
        self.layer[n].map_type.grid(row=0, column=3)


class Button(tk.Button):
    def __init__(self, master, window_mode):
        super().__init__(master,)


class Viewer_OneFrame:
    def __init__(self):
        # コントロールバー
        self.ctrlbar = None
        # 時間を進める
        self.btn_timepls = None
        # 時間
        self.btn_time = None
        # 時間を戻す
        self.btn_timeminus = None
        # 現在選択している画像の名前
        self.map_name = None
