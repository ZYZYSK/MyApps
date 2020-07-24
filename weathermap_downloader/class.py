import os
import datetime
DAYS_DURATION = 5  # 何日前のデータからダウンロードするか


class Map:
    def __init__(self, map_name, map_url):
        self.map_name = map_name  # 画像の種類
        self.map_url = map_url  # URL
        self.time = datetime.datetime.now()-datetime.timedelta(days=DAYS_DURATION)  # 開始時刻
        self.time_end = datetime.datetime.now()-datetime.timedelta(minutes=10)  # 終了時刻
        os.makedirs(self.map_name, exist_ok=True)  # フォルダの作成


class Map_radar(Map):
    def __init__(self, map_name, map_url):
        Map.__init__(self, map_name, map_url)

    def download_map(self):
        self.time.minute = (self.time.minute/5)*5

    def proceed_time(self):  # ファイルが存在しない時間まで時刻を進める
        while True:
            time_str = self.time.strftime('%Y%m%d%H%M')  # 時刻を文字列に変換
            # ファイルが存在しなければ終了
            if os.path.isfile(os.path.join(self.map_name, self.map_name + '_' + time_str + '.png')) == False:
                break
            self.time = datetime.datetime.strptime(
                time_str, '%Y%m%d%H%M')+datetime.timedelta(minuntes=5)  # 時刻を進める
