import tkinter as tk
from tkinter import ttk
import os
import sys


class Viewer_Base(tk.Frame):
    # 画像の種類
    jma_list = ['赤外(日本域)', '赤外(全球)', '可視(日本域)', '可視(全球)', '水蒸気(日本域)', '水蒸気(全球)', 'レーダー(日本域)', '天気図']
    gpv_list = ['300hPa高度、風', '500hPa高度、気温', '500hPa高度、渦度、風', '500hPa気温/700hPa湿数', '850hPa高度、気温', '850hPa気温、風/700hPa鉛直流', '850hPa相当温位']
    map_list = ['---'] + jma_list + gpv_list
    # ウィンドウタイトル
    window_title = 'Weather Viewer'
    # 解像度
    resolution = '1920x1080'
    # 設定ファイルのパス
    settings_path = os.path.join(os.path.dirname(__file__), 'settings.txt')
    # 画像へのパス
    img_full_path = os.path.join(os.path.dirname(__file__), 'icons', 'fullscreen.png')
    img_vs_path = os.path.join(os.path.dirname(__file__), 'icons', 'vs.png')
    img_sp_path = os.path.join(os.path.dirname(__file__), 'icons', 'sp.png')
    img_multi_path = os.path.join(os.path.dirname(__file__), 'icons', 'multi.png')
    # データのパス
    jma_path = None
    gpv_path = None
    # ツールバーの高さ
    toolbar_height = 30
    # コントロールバーの高さ
    ctrlbar_height = 20
    @classmethod
    def exit_program(cls, e, info=None):  # プログラムを終了させる
        if not info is None:
            exc_type, exc_obj, exc_tb = info
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno, '行目')
        print(e)
        print('\'q\'で終了します')
        while True:
            s = input()
            if s == 'q':
                sys.exit()

    @classmethod
    def get_settings(cls):  # 設定情報を取得する
        try:
            with open(cls.settings_path, mode='r') as f:
                paths = [s.strip() for s in f.readlines()]
                if len(paths) != 2:
                    cls.exit_program(cls.settings_path + ' の内容が正しくありません')
        except FileNotFoundError:
            cls.exit_program(cls.settings_path + ' が見つかりません')
        else:
            cls.jma_path = paths[0]; cls.gpv_path = paths[1]

    def __init__(self, master=None):
        # root
        super().__init__(master)
        self.pack()
        master.geometry('1920x1080')
        master.title('Weather Viewer')
        master.update_idletasks()
        # 全体画面
        self.frame_base = tk.Frame(master, bd=0, relief='solid')
        self.frame_base.pack(expand=True, fill=tk.BOTH)
        self.frame_base.update_idletasks()
        # ツールバー
        self.toolbar = tk.Frame(self.frame_base, bd=1, relief='solid')
        self.toolbar.pack(expand=False, anchor=tk.N, fill=tk.X)
        self.toolbar.update_idletasks()
        # ツールバーのボタン
        self.img_full = tk.PhotoImage(file=self.img_full_path)
        self.btn_full = tk.Button(self.toolbar, width=self.toolbar_height, image=self.img_full)
        self.btn_full.grid(row=0, column=0)
        self.img_vs = tk.PhotoImage(file=self.img_vs_path)
        self.btn_vs = tk.Button(self.toolbar, width=self.toolbar_height, image=self.img_vs)
        self.btn_vs.grid(row=0, column=1)
        self.img_sp = tk.PhotoImage(file=self.img_sp_path)
        self.btn_sp = tk.Button(self.toolbar, width=self.toolbar_height, image=self.img_sp)
        self.btn_sp.grid(row=0, column=2)
        self.img_multi = tk.PhotoImage(file=self.img_multi_path)
        self.btn_multi = tk.Button(self.toolbar, width=self.toolbar_height, image=self.img_multi)
        self.btn_multi.grid(row=0, column=3)
        # コントロールバー
        self.layer = [Viewer_OneFrame()] * 4
        # 画面
        self.show_full()

    def show_full(self):  # 全画面表示
        # 1画像につき表示する画面[フルスクリーン]
        self.frame_full = tk.Frame(self.frame_base, bd=0, relief='solid')
        self.frame_full.pack(expand=True, anchor=tk.N, fill=tk.BOTH)
        self.frame_full.update_idletasks()
        self.show_set(self.frame_full, 0)

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


class Viewer_OneFrame:
    def __init__(self):
        self.ctrlbar = None
        self.btn_timepls = None
        self.btn_time = None
        self.btn_timeminus = None
        self.map_type = None
        self.map_name = None
