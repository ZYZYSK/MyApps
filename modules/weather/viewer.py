import tkinter as tk
from tkinter import ttk
import json
import os
import sys
import logging
import signal

from ..functions import exit_program, handler_sigint

# ログ出力の無効化
# logging.disable(logging.CRITICAL)
# ログ出力設定
logging.basicConfig(level=logging.WARNING, format='%(levelname)s: %(message)s')

# 境界線の太さ
BORDER_DEBUG = 50
BORDER_RELEASE = 1


def viewer():
    logging.basicConfig(level=logging.WARNING, format='%(levelname)s: %(message)s')
    # SIGINTシグナルを受け取る
    signal.signal(signal.SIGINT, handler_sigint)
    # 設定情報の取得
    ViewerBase.get_settings()
    # 画面表示
    win = tk.Tk()
    app = ViewerBase(master=win)
    app.mainloop()


class ViewerBase(ttk.Frame):
    # 設定ファイルのパス
    settings_path = os.path.join(os.path.dirname(__file__), "viewer_settings.json")
    # 設定情報
    settings = None
    #アイコンへのパス: app
    icn_app = os.path.join(os.path.dirname(__file__), 'icons', 'app.ico')

    #アイコンへのパス: toolbar1
    icn_time_change = os.path.join(os.path.dirname(__file__), 'icons', 'time_change.png')
    icn_time_change_disabled = os.path.join(os.path.dirname(__file__), 'icons', 'time_change_disabled.png')

    # アイコンへのパス: toolbar2
    icn_pane1 = os.path.join(os.path.dirname(__file__), 'icons', 'pane1.png')
    icn_pane2v = os.path.join(os.path.dirname(__file__), 'icons', 'pane2v.png')
    icn_pane2h = os.path.join(os.path.dirname(__file__), 'icons', 'pane2h.png')
    icn_pane4 = os.path.join(os.path.dirname(__file__), 'icons', 'pane4.png')
    icn_pane4 = os.path.join(os.path.dirname(__file__), 'icons', 'pane4.png')
    icn_setting = os.path.join(os.path.dirname(__file__), 'icons', 'setting.png')

    @classmethod
    def get_settings(cls):  # 設定情報を取得する
        # 設定ファイルを読み込む
        try:
            with open(cls.settings_path, mode='r', encoding="utf-8") as f:
                cls.settings = json.load(f)

        # 設定ファイルが存在しない場合
        except FileNotFoundError:
            ("[エラー] 設定ファイルが見つかりません: {0}".format(cls.settings_path))

        # ファイルオープンエラー
        except Exception as e:
            exit_program(e, sys.exc_info())

        else:
            for i in cls.settings:
                logging.warning("\t{0}: {1}".format(i, cls.settings[i]))

    def __init__(self, master=None):
        # 初期設定
        super().__init__(master)
        self.pack()

        # ルートウィンドウの設定: タイトルバーの名前
        master.title(self.settings["window_title"])
        # ルートウィンドウの設定: 解像度
        master.geometry(self.settings["resolution"])
        # ルートウィンドウの設定: 最小ウィンドウサイズ
        master.minsize(self.settings["min_size"][0], self.settings["min_size"][1])
        # ルートウィンドウの設定: アイコン画像
        master.iconbitmap(self.icn_app)

        # アイコンの読み込み
        self.img_time_change = tk.PhotoImage(file=self.icn_time_change)
        self.img_time_change_disabled = tk.PhotoImage(file=self.icn_time_change_disabled)
        self.img_pane1 = tk.PhotoImage(file=self.icn_pane1)
        self.img_pane2h = tk.PhotoImage(file=self.icn_pane2h)
        self.img_pane2v = tk.PhotoImage(file=self.icn_pane2v)
        self.img_pane4 = tk.PhotoImage(file=self.icn_pane4)
        self.img_setting = tk.PhotoImage(file=self.icn_setting)

        # base_pane
        self.basepane = ttk.Frame(master)
        self.basepane.pack(expand=1, fill=tk.BOTH)

        # ツールバーの文字の大きさ
        self.toolbar_style = ttk.Style()
        self.toolbar_style.configure('ToolbarFontSize.TButton', font=('Yu Gothic', 20))

        #toolpane: toolbar1とtoolbar2の統合フレーム
        self.toolpane = ttk.Frame(self.basepane)
        self.toolpane.pack(anchor=tk.NW, expand=0, fill=tk.X, side=tk.TOP)

        # toolbar1
        self.toolbar1 = ttk.Frame(self.toolpane)
        self.toolbar1.pack(anchor=tk.W, expand=1, fill=tk.X, padx=5, pady=5, side=tk.LEFT)
        self.set_toolbar1_disabled()

        # toolbar2
        self.toolbar2 = ttk.Frame(self.toolpane)
        self.toolbar2.pack(anchor=tk.E, expand=0, fill=tk.NONE, padx=5, pady=5, side=tk.LEFT)
        self.set_toolbar2()

        #allpane: paneの統合フレーム
        self.allpane = ttk.Frame(self.basepane, relief='raised', borderwidth=1)
        self.allpane.pack(anchor=tk.SW, expand=1, fill=tk.BOTH, side=tk.TOP)

        # pane格納用
        self.panes = []

        # 最初は全画面表示
        self.set_pane1()

    def set_toolbar1_disabled(self):  # toolbar1(非アクティブ)
        # 「日時を戻す」ボタン
        self.btn_time_minus = ttk.Button(self.toolbar1, text='<', style='ToolbarFontSize.TButton', width=5)
        self.btn_time_minus.pack(anchor=tk.W, side=tk.LEFT)
        self.btn_time_minus.state(['disabled'])

        # 「現在日時」ラベル
        self.btn_time_now = ttk.Button(self.toolbar1, text='---- / ----  -- : --', style='ToolbarFontSize.TButton')
        self.btn_time_now.state(['disabled'])
        self.btn_time_now.pack(anchor=tk.W, side=tk.LEFT)

        # 「日時切り替え」ボタン
        logging.warning(self.icn_time_change)
        self.btn_time_change = ttk.Label(self.toolbar1, image=self.img_time_change_disabled, style='ToolbarFontSize.TButton', width=5)
        self.btn_time_change.pack(anchor=tk.W, side=tk.LEFT)

        # 「日時を進める」ボタン
        self.btn_time_plus = ttk.Button(self.toolbar1, text='>', style='ToolbarFontSize.TButton', width=5)
        self.btn_time_plus.pack(anchor=tk.W, side=tk.LEFT)
        self.btn_time_plus.state(['disabled'])

    def set_toolbar2(self):  # toolbar2(常にアクティブ)
        # 全画面表示
        self.btn_pane1 = ttk.Button(self.toolbar2, image=self.img_pane1, style='ToolbarFontSize.TButton')
        self.btn_pane1.pack(anchor=tk.E, side=tk.LEFT)

        # 2縦表示
        self.btn_pane2v = ttk.Button(self.toolbar2, image=self.img_pane2v, style='ToolbarFontSize.TButton')
        self.btn_pane2v.pack(anchor=tk.E, side=tk.LEFT)

        # 2横表示
        self.btn_pane2h = ttk.Button(self.toolbar2, image=self.img_pane2h, style='ToolbarFontSize.TButton')
        self.btn_pane2h.pack(anchor=tk.E, side=tk.LEFT)

        # 4画面表示
        self.btn_pane4 = ttk.Button(self.toolbar2, image=self.img_pane4, style='ToolbarFontSize.TButton')
        self.btn_pane4.pack(anchor=tk.E, side=tk.LEFT)

        # 設定
        self.btn_setting = ttk.Button(self.toolbar2, image=self.img_setting, style='ToolbarFontSize.TButton')
        self.btn_setting.pack()

    def set_pane1(self):  # 全画面表示
        # 起動時の場合
        if len(self.panes) == 0:
            self.panes.append(OnePane(0, 0, self.settings, self.allpane))

        # 前回の表示が2画面以上の場合
        elif len(self.panes) > 1:
            pass


class OnePane(ttk.Frame):  # 1つのPaneFrameクラス
    def __init__(self, column, row, settings, master=None):
        # Frame
        super().__init__(master)
        master.columnconfigure(column, weight=1)
        master.rowconfigure(row, weight=1)
        self.grid(column=column, row=row, sticky=tk.W + tk.E + tk.N + tk.S)

        # 画像の種類一覧
        self.map_types = list(settings['jma_list'].keys()) + list(settings['gpv_list'].keys())
        logging.warning(self.map_types)
        if len(self.map_types) == 0:
            exit_program("[エラー] 画像の種類(jma_list,gpv_list)の設定が正しくありません．")

        #Toolbar: 画像の種類を指定できるCombobox
        self.toolbar_text = tk.StringVar()
        self.cb_toolbar = ttk.Combobox(self, textvariable=self.toolbar_text, values=self.map_types, height=10)
        self.cb_toolbar.pack(anchor=tk.N, expand=0, fill=tk.X, side=tk.TOP)

        #Canvas: 画像を載せる
        self.canvas = tk.Canvas(self, bg='black')
        self.canvas.pack(anchor=tk.N, expand=1, fill=tk.BOTH, padx=0, pady=0, side=tk.TOP)
