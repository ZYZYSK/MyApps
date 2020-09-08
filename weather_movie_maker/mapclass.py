import os
import threading
import datetime
import cv2
from func import *


class Map:
    def __init__(self, map_name, interval, time_list, save_path, fps):
        # 画像の種類
        self.map_name = map_name
        # 日時の間隔
        self.interval = interval
        # 開始日時
        self.time_start = datetime.datetime.strptime(
            time_list[0], "%Y%m%d%H%M")
        # 終了日時
        self.time_end = datetime.datetime.strptime(
            time_list[1], "%Y%m%d%H%M")
        # 保存先
        self.save_path = save_path
        # fps
        self.fps = fps

    def make_video(self):
        time_now = self.time_start
        # 先頭のファイル名
        if self.map_name == 'weather_map':
            file_name = os.path.join(self.map_name, self.map_name+'_' +
                                     self.time_start.strftime('%Y%m%d%H')[2:]+'.png')
        else:
            file_name = os.path.join(self.map_name, self.map_name+'_' +
                                     self.time_start.strftime('%Y%m%d%H%M')+'.png')
        # 先頭のファイルを開く
        img = cv2.imread(file_name, 1)
        if img is None:
            exit_program(img+':ファイルが存在しません')
        # 解像度のy
        height = img.shape[0]
        # 解像度のx
        width = img.shape[1]
        # ビデオ名
        video_name = os.path.join(
            self.save_path, self.map_name + '.mp4')
        # 同じ名前のビデオが存在する場合
        if os.path.isfile(video_name):
            while True:
                print(self.map_name+':同じファイルが存在しますが上書きしますか？(y/n):')
                s = input().lower()
                if s == 'y':
                    break
                elif s == 'n':
                    return
        # ビデオ情報を表示
        print('名前:'+video_name+', 解像度:' + str(width) + 'X' +
              str(height) + ', fps:'+str(self.fps))
        # mp4形式で作成
        fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
        # ビデオ情報を設定
        video = cv2.VideoWriter(video_name, fourcc, self.fps, (width, height))
        # ビデオ作成
        while (time_now <= self.time_end):
            # ファイル名の設定
            if self.map_name == 'weather_map':
                cname = os.path.join(self.map_name, self.map_name+'_' +
                                     time_now.strftime('%Y%m%d%H')[2:]+'.png')
            else:
                cname = os.path.join(self.map_name, self.map_name+'_' +
                                     time_now.strftime('%Y%m%d%H%M')+'.png')
            # 画像を開く
            cimg = cv2.imread(cname, 1)
            # 日時を進める
            time_now = time_now + datetime.timedelta(minutes=self.interval)
            # 画像を開けない場合や、画像が正しくない場合
            if (cimg is None) or (cimg.shape[0] != height) or (cimg.shape[1] != width):
                print(cname+':ファイルが存在しないか、正しくありません')
                continue
            # 画像をビデオに書き込む
            video.write(cimg)
            # 進歩率を表示
            if time_now.day % 3 == 0 and time_now.hour == 0 and time_now.minute == 0:
                progress = int((time_now - self.time_start) /
                               (self.time_end - self.time_start) * 100)
                print(self.map_name+':'+str(progress).rjust(3, ' ')+'%完了しました')
        # ビデオを閉じる
        video.release()
        print(self.map_name+':100%完了しました')


class Map_run(threading.Thread):
    def __init__(self, map_name, interval, time_list, save_path, fps):
        threading.Thread.__init__(self)
        self.A = Map(map_name, interval, time_list, save_path, fps)

    def run(self):
        self.A.make_video()
