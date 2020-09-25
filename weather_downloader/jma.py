import os
import shutil
import sys
import datetime
import time as tm
import requests
import urllib
from concurrent import futures


class JMA:
    # 設定ファイルの場所
    settings_file_path = os.path.join(os.path.dirname(__file__), 'jma_settings.txt')
    # 何日前から
    days_duration = 6
    # 保存場所
    path = None

    @classmethod
    def get_settings(cls):  # 画像の保存場所の情報を取得
        try:
            f = open(cls.settings_file_path, mode='r')
        except FileNotFoundError:
            f = open(cls.settings_file_path, mode='w')
            f.write('.')
            f.close()
            f = open(cls.settings_file_path, mode='r')
        except Exception as e:
            cls.exit_program(e, sys.exc_info())
        finally:
            cls.path = f.readline()
            print('保存先：' + cls.path)
            f.close()

    @classmethod
    def move_path(cls):    # データの保存場所に移動
        try:
            os.makedirs(cls.path, exist_ok=True)
            os.chdir(cls.path)
        except FileNotFoundError:
            cls.exit_program('指定されたパスは正しくありません. jma_settings.txtを正しく設定してください.')
        except Exception as e:
            cls.exit_program(e, sys.exc_info())

    @classmethod
    def exit_program(cls, e, info=None):  # プログラムの終了
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
    def check_connection(cls):  # ネット接続が確立されるまで待機
        while True:
            # ネット接続を確認
            try:
                urllib.request.urlopen('https://www.jma.go.jp/jma/index.html')
            except Exception as e:
                print(e)
                tm.sleep(10)
            else:
                break

    @classmethod
    def check_is_on_server(cls, url):  # ダウンロードするファイルがサーバーに存在するか確認
        try:
            urllib.request.urlopen(url)
        except Exception:
            return False
        else:
            return True

    @classmethod
    def download_file(cls, time, map_name, map_url, interval):  # 個々のファイルを取得
        # 日時を文字列に変換
        time_str = time.strftime('%Y%m%d%H%M')
        # ファイル名を取得
        file_name = os.path.join(map_name, map_name + '_' + time_str + '.png')
        # ファイルが存在すれば何もしない
        if os.path.exists(file_name):
            return
        # URLの作成
        url = map_url + time_str + '-00.png'
        # ネット接続が確立されるまで待機
        cls.check_connection()
        # ダウンロードするファイルが存在する場合
        if cls.check_is_on_server(url):
            while True:
                # ダウンロード試行
                try:
                    req = requests.get(url, timeout=10)
                # ダウンロードできない場合：
                except Exception as e:
                    print(e)
                    tm.sleep(10)
                # ダウンロードが成功したらファイルを保存
                else:
                    print('[ダウンロード] ' + file_name)
                    with open(file_name, 'wb') as fp:
                        fp.write(req.content)
                    break
        # ダウンロードするファイルが存在しない場合
        else:
            # interval分前のファイルが存在する場合
            try:
                shutil.copy(os.path.join(map_name, map_name + '_' + (time - datetime.timedelta(minutes=interval)).strftime('%Y%m%d%H%M') + '.png'), file_name)
            # interval分前のファイルが存在しない場合
            except FileNotFoundError:
                pass
            except Exception as e:
                cls.exit_program(e, sys.exc_info())
            # コピーが成功したことを表示
            else:
                print('[コピー　　　] ' + file_name)

    def __init__(self, map_name, map_url, interval):  # 初期化
        # 画像の種類
        self.map_name = map_name
        # URL
        self.map_url = map_url
        # 日時の間隔(分)
        self.interval = interval
        # 開始日時
        self.time_now = datetime.datetime.now() - datetime.timedelta(days=self.days_duration)
        # 開始日時をintervalの倍数に変換
        if self.interval <= 60:
            self.time_now = datetime.datetime(self.time_now.year, self.time_now.month, self.time_now.day, self.time_now.hour, self.time_now.minute // self.interval * self.interval)
        elif self.interval > 60 and self.interval % 60 == 0:
            self.time_now = datetime.datetime(self.time_now.year, self.time_now.month, self.time_now.day, self.time_now.hour // (self.interval // 60) * (self.interval // 60), 00)
        # 終了日時
        self.time_end = datetime.datetime.now() - datetime.timedelta(minutes=self.interval)
        # フォルダの作成
        os.makedirs(self.map_name, exist_ok=True)

    def download_map(self):  # 現在日時までのファイルをダウンロード
        while self.time_now <= self.time_end:
            self.download_file(self.time_now, self.map_name, self.map_url, self.interval)
            # 日時を進める
            self.time_now += datetime.timedelta(minutes=self.interval)


class JMA_weathermap(JMA):  # 天気図ダウンロード用
    def __init__(self, map_name, map_url, interval):
        # 初期化
        JMA.__init__(self, map_name, map_url, interval)

    @classmethod
    def download_file(cls, time, map_name, map_url, interval):  # 個々のファイルを取得
        # 日時を文字列に変換して調整
        time_str = time.strftime('%Y%m%d%H')
        time_str = time_str[2:]
        # ファイル名を取得
        file_name = os.path.join(map_name, map_name + '_' + time_str + '.png')
        # ファイルが存在すれば何もしない
        if os.path.exists(file_name):
            return
        # URLを作成
        url = map_url + time_str + '.png'
        # 0時のファイルを取得する場合
        if time_str[(len(time_str) - 2):] == '00':
            # 3時間前の日時を文字列に変換
            time_str_before = (time - datetime.timedelta(hours=3)).strftime('%Y%m%d%H')
            time_str_before = time_str_before[2:]
            # 3時間前の日時のファイル名を取得
            file_name_before = os.path.join(map_name, map_name + '_' + time_str_before + '.png')
            # 3時間前のファイルをが存在する場合
            try:
                shutil.copy(file_name_before, file_name)
            # 3時間前のファイルも存在しない場合は何もしない
            except FileNotFoundError:
                pass
            except Exception as e:
                cls.exit_program(e, sys.exc_info())
            # コピーが成功したことを表示
            else:
                print('[コピー　　　] ' + file_name)
        # 0時以外のファイルを取得する場合
        else:
            # ネット接続が確立されるまで待機
            cls.check_connection()
            # ダウンロードしたいファイルがサーバーにある場合
            if (cls.check_is_on_server(url)):
                while True:
                    # ダウンロード試行
                    try:
                        req = requests.get(url, timeout=10)
                    # ダウンロードできない場合
                    except Exception as e:
                        print(e)
                        tm.sleep(10)
                    # ダウンロード成功したらファイルを保存
                    else:
                        print('[ダウンロード] ' + file_name)
                        with open(file_name, "wb") as fp:
                            fp.write(req.content)
                        break
