import os
import sys
import re
import logging
import signal
import datetime
import json
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox

import sqlite3

from ..functions import exit_program_tk, handler_sigint_tk

# ログ出力の無効化
logging.disable(logging.CRITICAL)
# ログ出力設定
logging.basicConfig(level=logging.WARNING, format='%(levelname)s: %(message)s')


def temperature_loader():
    # SIGINTシグナルを受け取る
    signal.signal(signal.SIGINT, handler_sigint_tk)
    # 設定情報の取得
    Temperature.get_settings()
    # 画面表示
    win = tk.Tk()
    app = OpenDialog(master=win)
    app.mainloop()


class OpenDialog(ttk.Frame):
    # アイコンへのパス: app_temp.ico
    icn_app = os.path.join(os.path.dirname(__file__), 'icons', 'app_temp.ico')

    def __init__(self, master=None):
        # 初期設定
        super().__init__(master)
        self.pack()
        self.master = master
        # ルートウィンドウの設定: タイトルバーの名前
        master.title("Temperature Loader")
        # ルートウィンドウの設定: 最小ウィンドウサイズ
        master.minsize(200, 50)
        # ルートウィンドウの設定: ウィンドウサイズ変更禁止
        master.resizable(0, 0)
        # ルートウィンドウの設定: アイコン画像
        master.iconbitmap(self.icn_app)
        # base_window
        self.basewindow = ttk.Frame(master)
        self.basewindow.pack(expand=0, fill=tk.NONE)
        # 文字の大きさ
        self.btn_style = ttk.Style()
        self.btn_style.configure("BtnStyle.TButton", font=('Yu Gothic', 20))
        # 「開く」ボタン
        self.btn = ttk.Button(self.basewindow, text="Open...(O)", style="BtnStyle.TButton")
        self.btn.pack()
        # ボタン設定
        master.bind(sequence="<Key-o>", func=self.set_btn)
        self.btn.bind(sequence="<ButtonRelease-1>", func=self.set_btn)

    def set_btn(self, event):  # ファイルを開き，内容をデータベースに格納する
        file = filedialog.askopenfile(initialdir=os.path.dirname(__file__), filetypes=[("テキストファイル", "*.txt")])
        # ファイルを開けたら
        if file:
            # 読み込み
            new_temperature = Temperature(file, self.master)
            # 読み込み
            new_temperature.load()
            # データの加工
            new_temperature.operate()
            # データベースへの格納
            new_temperature.insert()
            # メッセージボックスの表示
            if new_temperature.changed:
                messagebox.showinfo("情報", "{0}に書き込みました．\n詳しくは\"{1}\"を参照してください．".format(new_temperature.settings["db_path"], new_temperature.settings["log_dir_path"]))
            else:
                messagebox.showerror("エラー", "{0}に何も書き込みませんでした．\n詳しくは\"{1}\"を参照してください．".format(new_temperature.settings["db_path"], new_temperature.settings["log_dir_path"]))

            # ログの出力
            new_temperature.save_log()


class Temperature():
    # 設定ファイルのパス
    settings_path = os.path.join(os.path.dirname(__file__), "temperature_settings.json")
    # 設定情報
    settings = None

    @classmethod
    def get_settings(cls):  # 設定情報を取得する
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

    def __init__(self, file_object, master=None):
        # ルートウィンドウ
        self.master = master
        # 読み込むファイルの内容
        self.file_object = file_object
        # 読み込むデータの格納先
        self.new_data = []
        # 挿入できなかった日時とデータのリスト
        self.error_data = []
        # 補正が必要な日時かどうか
        self.need_change = True
        # データベースに書き込まれたかどうか
        self.changed = False

    def load(self):  # 読み込みの開始
        # 読み込み
        try:
            l = [i.strip() for i in self.file_object.readlines()]
            for i in l:
                new_i = i.split()
                if len(new_i) == 4:
                    # 各行の先頭の文字(空白を除く)
                    try:
                        integer = int(new_i[0])
                    # 数値でなければ格納しない
                    except ValueError:
                        pass
                    except Exception as e:
                        exit_program_tk("エラー", "{0}\n{1}".format(e, sys.exc_info()), self.master)
                    # 数値であれば格納する
                    else:
                        self.new_data.append(new_i[1:])
        # ファイルを読み込めない場合
        except IndexError:
            exit_program_tk("エラー", "txtファイルを正しく読み込めません．", self.master)
        except Exception as e:
            exit_program_tk("エラー", "{0}\n{1}".format(e, sys.exc_info()), self.master)

    def operate(self):  # 読み込んだデータの加工
        for data in self.new_data:
            try:
                # 文字列を日付に変換
                data_date = datetime.datetime.strptime(data[0], "%Y/%m/%d")
                # 日付を文字列に変換
                data[0] = data_date.strftime("%Y-%m-%d")
                # 文字列を時刻に変換
                data_time = datetime.datetime.strptime(data[1], "%H:%M:%S")
                # 時刻補正(5分ごとにする)
                data_time = datetime.time(data_time.hour, data_time.minute // self.settings["interval"] * self.settings["interval"])
                # 補正後の時刻を格納
                data[1] = data_time.strftime("%H-%M")
                # 温度を文字列から小数に変換
                data[2] = float(data[2])
            except Exception as e:
                exit_program_tk("エラー", "{0}\n{1}".format(e, sys.exc_info()), self.master)

    def insert(self):  # データベースへの格納
        # データベースへの接続
        try:
            os.makedirs(os.path.dirname(self.settings["db_path"]), exist_ok=True)
        # データベースへのパスが正しくない場合
        except FileNotFoundError:
            exit_program_tk("エラー", "{0}: \"db_path\"は有効なパスではありません．".format(self.settings_path))
        except Exception as e:
            exit_program_tk("エラー", "{0}\n{1}".format(e, sys.exc_info()), self.master)
        self.db = sqlite3.connect(self.settings["db_path"])
        self.cur = self.db.cursor()
        # 作成されていなければテーブルの作成
        self.cur.execute("CREATE TABLE IF NOT EXISTS Temperature(date text,time text,temperature real,PRIMARY KEY(date,time));")
        # データの挿入
        for i in range(0, len(self.new_data)):
            # 重複がある場合
            if self.is_conflict(self.new_data[i][0], self.new_data[i][1]):
                # エラーリストに追加
                self.error_data.append(self.new_data[i] + ["重複エラー"])
            # 重複がない場合
            else:
                logging.warning("重複なし")
                # 各データの挿入
                try:
                    # 補正が必要なデータの場合
                    if self.need_change:
                        # 今回追加する最初のデータだけ補正が必要
                        self.need_change = False
                        old_data = self.new_data[i][2]
                        if i == 0 and i + 1 < len(self.new_data):
                            self.new_data[i][2] = self.new_data[i + 1][2]
                        elif i > 0 and i + 1 < len(self.new_data):
                            self.new_data[i][2] = (self.new_data[i - 1][2] + self.new_data[i + 1][2]) / 2
                    # 挿入
                    sql = "INSERT INTO Temperature VALUES('{0}','{1}',{2});".format(self.new_data[i][0], self.new_data[i][1], self.new_data[i][2])
                    self.cur.execute(sql)
                # 挿入できない場合(NULL制約など)
                except sqlite3.IntegrityError as e:
                    self.error_data.append(self.new_data[i] + [e])
                except Exception as e:
                    exit_program_tk("エラー", "{0}\n{1}".format(e, sys.exc_info()), self.master)
                else:
                    # 書き込み操作が行われた
                    self.changed = True
        # 変更をコミット
        self.db.commit()
        # 閉じる
        self.db.close()

    def is_conflict(self, data_date, data_time):  # 重複確認
        # 重複を検索
        sql = "SELECT * FROM Temperature WHERE date='{0}' AND time='{1}'".format(data_date, data_time)
        self.cur = self.db.execute(sql)
        # 重複があればTrue
        if len(self.cur.fetchall()):
            return True
        # 重複がなければFalse
        else:
            return False

    def save_log(self):  # 変更したデータと挿入できなかったデータのリストを出力
        # ログ出力先フォルダがなければ作成
        try:
            os.makedirs(self.settings["log_dir_path"], exist_ok=True)
        except FileNotFoundError:
            messagebox.showerror("エラー", "{0}: \"log_dir_path\"は有効なパスではありません．".format(self.settings_path))
        except Exception as e:
            exit_program_tk("エラー", "{0}\n{1}".format(e, sys.exc_info()), self.master)
        # ログのファイル名
        log_path = os.path.join(self.settings["log_dir_path"], "temperature_loader_{0}.log".format(datetime.datetime.now().strftime("%Y%m%d_%H%M%S")))
        try:
            with open(log_path, mode="w") as f:
                # 変更したデータのリスト
                for i in self.error_data:
                    # 挿入したデータリスト
                    f.write("[挿入に失敗したデータ:{3}] {0} {1}: {2}\n".format(i[0], i[1], i[2], i[3]))
        except Exception as e:
            messagebox.showwarning("警告", "ログが正しく出力されませんでした．\n{0}\n{1}".format(e, sys.exc_info()))
