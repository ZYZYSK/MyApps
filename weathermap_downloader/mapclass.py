import os
import shutil
import sys
import datetime
import requests
import threading
from func import *
DAYS_DURATION = 6  # 何日前のデータからダウンロードするか


class Map:
    def __init__(self, map_name, map_url, interval):  # 初期化
        # 画像の種類
        self.map_name = map_name
        # URL
        self.map_url = map_url
        # 日時の間隔
        self.interval = interval
        # 開始日時
        self.time = datetime.datetime.now()-datetime.timedelta(days=DAYS_DURATION)
        # 日時をintervalの倍数に変換
        if self.interval <= 60:
            self.time = datetime.datetime(self.time.year, self.time.month, self.time.day,
                                          self.time.hour, self.time.minute//self.interval*self.interval)
        elif self.interval > 60 and self.interval % 60 == 0:
            self.time = datetime.datetime(
                self.time.year, self.time.month, self.time.day, self.time.hour//(self.interval//60)*(self.interval//60), 00)
        # 終了日時
        self.time_end = datetime.datetime.now(
        )-datetime.timedelta(minutes=self.interval)
        # フォルダの作成
        os.makedirs(self.map_name, exist_ok=True)


class Map_default(Map):
    def __init__(self, map_name, map_url, interval):
        # 初期化
        Map.__init__(self, map_name, map_url, interval)

    def download_map(self):
        # 現在日時までのファイルをダウンロード
        while(self.time_end >= self.time):
            # 日時を文字列に変換
            time_str = self.time.strftime('%Y%m%d%H%M')
            # URLを取得
            url = self.map_url+time_str+'-00.png'
            # ファイル名を取得
            name = os.path.join(self.map_name, self.map_name +
                                '_'+time_str+'.png')
            # インターネット接続を確認
            check_connection()
            # ダウンロードしたいファイルがサーバーにある場合
            if (check_is_on_server(url)):
                # ファイルをダウンロード
                try:
                    req = requests.get(url, timeout=10)
                # ダウンロード失敗したらやり直し
                except Exception as e:
                    print(e)
                    continue
                # ダウンロード成功したらファイルを保存
                else:
                    with open(name, "wb") as fp:
                        fp.write(req.content)
                        fp.close()
                    print('ダウンロード：'+name)
            # ダウンロードしたいファイルがサーバーにない場合
            else:
                # interval分前のファイルを名前を現在の時間にして複製
                try:
                    shutil.copy(os.path.join(self.map_name, self.map_name+'_'+(self.time-datetime.timedelta(
                        minutes=self.interval)).strftime('%Y%m%d%H%M')+'.png'), name)
                # interval分前のファイルも存在しない場合
                except FileNotFoundError:
                    pass
                except Exception as e:
                    exit_program(e, sys.exc_info())
                # コピーが成功したことを表示
                else:
                    print('コピー　　　：'+name)
            # 日時を進める
            self.time += datetime.timedelta(minutes=self.interval)

    def proceed_time(self):  # ファイルが存在しない時間まで日時を進める
        while True:
            # 日時を文字列に変換
            time_str = self.time.strftime('%Y%m%d%H%M')
            # ファイルが存在しなければ日時を進めるのをストップ
            if os.path.isfile(os.path.join(self.map_name, self.map_name + '_' + time_str + '.png')) == False:
                break
            # 日時を進める
            self.time += datetime.timedelta(minutes=self.interval)


class Map_weather_map(Map):  # 天気図ダウンロード用
    def __init__(self, map_name, map_url, interval):
        # 初期化
        Map.__init__(self, map_name, map_url, interval)

    def download_map(self):
        # 現在日時までのファイルをダウンロード
        while(self.time_end >= self.time):
            # 日時を文字列に変換して調整
            time_str = self.time.strftime('%Y%m%d%H')
            time_str = time_str[2:]
            # URLを取得
            url = self.map_url+time_str+'.png'
            # ファイル名を取得
            name = os.path.join(
                self.map_name, self.map_name + '_'+time_str+'.png')
            # 0時のファイルを取得する場合
            if time_str[(len(time_str) - 2):] == '00':
                # 3時間前の日時を文字列に変換
                time_str_before = (
                    self.time-datetime.timedelta(hours=3)).strftime('%Y%m%d%H')
                time_str_before = time_str_before[2:]
                # 3時間前の日時のファイル名を取得
                name_before = os.path.join(
                    self.map_name, self.map_name+'_'+time_str_before+'.png')
                # 3時間前のファイルをコピーして0時に改名
                try:
                    shutil.copy(name_before, name)
                # 3時間前のファイルも存在しない場合は何もしない
                except FileNotFoundError:
                    pass
                except Exception as e:
                    exit_program(e, sys.exc_info())
                # コピーが成功したことを表示
                else:
                    print('コピー　　　：'+name)
            # 0時以外のファイルを取得する場合
            else:
                # インターネット接続を確認
                check_connection()
                # ダウンロードしたいファイルがサーバーにある場合
                if (check_is_on_server(url)):
                    # ファイルをダウンロード
                    try:
                        req = requests.get(url, timeout=10)
                    # ダウンロード失敗したらやり直し
                    except Exception as e:
                        print(e)
                        continue
                    # ダウンロード成功したらファイルを保存
                    else:
                        with open(name, "wb") as fp:
                            fp.write(req.content)
                            fp.close()
                        print('ダウンロード：'+name)
            # 日時を進める
            self.time += datetime.timedelta(minutes=self.interval)

    def proceed_time(self):  # ファイルが存在しない時間まで日時を進める
        while True:
            # 日時を文字列に変換して調整
            time_str = self.time.strftime('%Y%m%d%H')
            time_str = time_str[2:]
            if os.path.isfile(os.path.join(self.map_name, self.map_name + '_' + time_str + '.png')) == False:
                break
            # 日時を進める
            self.time += datetime.timedelta(minutes=self.interval)


class Map_run(threading.Thread):
    def __init__(self, map_name, map_url, class_name, interval):
        threading.Thread.__init__(self)
        self.A = class_name(map_name, map_url, interval)

    def run(self):
        self.A.proceed_time()
        self.A.download_map()
