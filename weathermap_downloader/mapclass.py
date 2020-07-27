import os
import threading
import shutil
import requests
import datetime
from func1 import *
DAYS_DURATION = 5  # 何日前のデータからダウンロードするか


class Map:
    def __init__(self, map_name, map_url, interval):
        self.map_name = map_name  # 画像の種類
        self.map_url = map_url  # URL
        self.interval = interval  # 時刻の間隔
        self.time = datetime.datetime.now()-datetime.timedelta(days=DAYS_DURATION)  # 開始時刻
        self.time_end = datetime.datetime.now(
        )-datetime.timedelta(minutes=self.interval)  # 終了時刻
        os.makedirs(self.map_name, exist_ok=True)  # フォルダの作成


class Map_default(Map):
    def __init__(self, map_name, map_url, interval):
        Map.__init__(self, map_name, map_url, interval)
        time_int = int(self.time.strftime('%Y%m%d%H%M'))  # 時刻を数字に変換
        time_int = time_int//self.interval*self.interval
        self.time = datetime.datetime.strptime(
            str(time_int), '%Y%m%d%H%M')  # 時刻をintervalの倍数に変換

    def download_map(self):
        while(self.time_end >= self.time):
            time_str = self.time.strftime('%Y%m%d%H%M')  # 時刻を文字列に変換
            url = self.map_url+time_str+'-00.png'  # URLを取得
            name = os.path.join(self.map_name, self.map_name +
                                '_'+time_str+'.png')  # ファイル名を取得
            check_connection()  # インターネット接続を確認
            if (check_is_on_server(url)):  # ダウンロードしたいファイルがサーバーにある場合
                try:
                    req = requests.get(url, timeout=10)  # ファイルをダウンロード
                except Exception as e:
                    print(e)
                    continue  # ダウンロード失敗したらやり直し
                else:  # ダウンロード成功したらファイルを保存
                    with open(name, "wb") as fp:
                        fp.write(req.content)
                        fp.close()
                    print('ダウンロード：'+name)
            else:  # ダウンロードしたいファイルがサーバーにない場合
                try:
                    shutil.copy(os.path.join(self.map_name, self.map_name+'_'+(self.time-datetime.timedelta(
                        minutes=self.interval)).strftime('%Y%m%d%H%M')+'.png'), name)  # interval分前のファイルを名前を現在の時間にして複製
                    print('コピー　　　：'+name)
                except FileNotFoundError:  # interval前のファイルも存在しない場合
                    pass
                except Exception as e:
                    exit_program(e)
            # 時刻を進める
            self.time += datetime.timedelta(minutes=self.interval)

    def proceed_time(self):  # ファイルが存在しない時間まで時刻を進める
        while True:
            time_str = self.time.strftime('%Y%m%d%H%M')  # 時刻を文字列に変換
            # ファイルが存在しなければ時刻を進めるのをストップ
            if os.path.isfile(os.path.join(self.map_name, self.map_name + '_' + time_str + '.png')) == False:
                break
            # 時刻を進める
            self.time += datetime.timedelta(minutes=self.interval)


class Map_default_run(threading.Thread):
    def __init__(self, map_name, map_url, class_name, interval):
        threading.Thread.__init__(self)
        self.A = class_name(map_name, map_url, interval)

    def run(self):
        self.A.proceed_time()
        self.A.download_map()
