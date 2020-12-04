import os
import sys
import re
import logging
import signal
import datetime
import json

import sqlite3

from .functions import exit_program, handler_sigint

# ログ出力の無効化
# logging.disable(logging.CRITICAL)
# ログ出力設定
logging.basicConfig(level=logging.WARNING, format='%(levelname)s: %(message)s')


def temperature_loader():
    # SIGINTシグナルを受け取る
    signal.signal(signal.SIGINT, handler_sigint)
    # 設定情報の取得
    TemperatureLoader.get_settings()
    # 読み込み
    try:
        new_temperature = TemperatureLoader(sys.argv[1])
    except IndexError:
        exit_program("コマンドライン引数の第1引数が空なので，読み込めませんでした．")
    # 読み込むファイルのチェック
    new_temperature.check_load_file()
    # 読み込み
    new_temperature.load()
    # データの加工
    new_temperature.operate()
    # データベースへの格納
    new_temperature.insert()


class TemperatureLoader():
    # 設定ファイルのパス
    settings_path = os.path.join(os.path.dirname(__file__), "temperature_settings.json")
    # 設定情報
    settings = None
    #アイコンへのパス: app
    icn_app = os.path.join(os.path.dirname(__file__), 'icons', 'app.ico')

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

    def __init__(self, load_file_path):
        # 読み込むファイルのパス
        self.load_file_path = load_file_path
        # 読み込むデータの格納先
        self.new_data = []

    def check_load_file(self):  # 読み込むファイルがtxt形式かどうかチェック
        # 読み込むファイルの拡張子をチェック
        is_txt = re.search('.+\.txt', self.load_file_path)
        logging.warning(self.load_file_path)
        # txt形式の場合
        if is_txt:
            logging.warning("正しく読み込めました．")
        # txt形式でない場合
        else:
            exit_program("指定したファイルはtxt形式ではないため，読み込めませんでした．")

    def load(self):  # 読み込みの開始
        # 読み込み
        try:
            with open(self.load_file_path, mode="r", encoding="iso8859_2") as f:
                l = [i.strip() for i in f.readlines()]
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
                            exit_program(e, sys.exc_info())
                        # 数値であれば格納する
                        else:
                            self.new_data.append(new_i[1:])
        # ファイルを開けない場合
        except FileNotFoundError:
            exit_program("指定されたファイルが存在しません．")
        # ファイルを読み込めない場合
        except IndexError:
            exit_program("ファイルを正しく読み込めません．")
        except Exception as e:
            exit_program(e, sys.exc_info())

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
                exit_program(e, sys.exc_info())

    def insert(self):  # データベースへの格納
        # データベースへの接続
        os.makedirs(os.path.dirname(self.settings["db_path"]), exist_ok=True)
        db = sqlite3.connect(self.settings["db_path"])
        cur = db.cursor()
        # 作成されていなければテーブルの作成
        cur.execute("CREATE TABLE IF NOT EXISTS Temperature(date text,time text,temperature real,PRIMARY KEY(date,time));")
        # データの挿入
        for i in self.new_data:
            # 各データの挿入
            try:
                sentence = "INSERT INTO Temperature VALUES('{0}','{1}',{2});".format(i[0], i[1], i[2])
                logging.warning(sentence)
                cur.execute(sentence)
            # 挿入できない場合(主キー制約など)
            except sqlite3.IntegrityError:
                print("({0},{1},{2})は挿入できませんでした．".format(i[0], i[1], i[2]))
        # 変更をコミット
        db.commit()
        # 閉じる
        db.close()
