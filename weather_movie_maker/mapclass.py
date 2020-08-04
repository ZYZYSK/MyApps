import os
import threading
import datetime
import cv2
from func import *


class Map:
    def __init__(self, map_name, interval, day_list, save_path, fps):
        self.map_name = map_name  # 画像の種類
        self.interval = interval  # 時刻の間隔
        self.time_start = datetime.datetime.strptime(
            day_list[0]+'0000', "%Y%m%d%H%M")  # 開始時刻
        if interval == 5:  # 終了時刻
            self.time_end = datetime.datetime.strptime(
                day_list[1]+'2355', "%Y%m%d%H%M")
        else:  # 終了時刻
            self.time_end = datetime.datetime.strptime(
                day_list[1]+'2350', "%Y%m%d%H%M")
        self.save_path = save_path  # 保存先
        self.fps = fps  # fps

    def make_video(self):
        time_now = self.time_start
        file_name = os.path.join(self.map_name, self.map_name+'_' +
                                 self.time_start.strftime('%Y%m%d%H%M')+'.png')  # 先頭のファイル名
        img = cv2.imread(file_name, 1)  # 先頭のファイルを開く
        if img is None:
            exit_program(img+':ファイルが存在しません')
        height = img.shape[0]  # 解像度のy
        width = img.shape[1]  # 解像度のx
        video_name = os.path.join(
            self.save_path, self.map_name + '.mp4')  # ビデオ名
        if os.path.isfile(video_name):
            while True:
                print(self.map_name+':同じファイルが存在しますが上書きしますか？(y/n):')
                s = input().lower()
                if s == 'y':
                    break
                elif s == 'n':
                    return
        print('名前:'+video_name+', 解像度:' + str(width) + 'X' +
              str(height) + ', fps:'+str(self.fps))
        fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
        video = cv2.VideoWriter(video_name, fourcc, self.fps, (width, height))
        while (time_now <= self.time_end):
            cname = os.path.join(self.map_name, self.map_name+'_' +
                                 time_now.strftime('%Y%m%d%H%M')+'.png')  # /ファイル名
            # print(cname)
            cimg = cv2.imread(cname, 1)
            time_now = time_now + datetime.timedelta(minutes=self.interval)
            if (cimg is None) or (cimg.shape[0] != height) or (cimg.shape[1] != width):
                print(cname+':ファイルが存在しないか、正しくありません')
                continue
            video.write(cimg)
            if time_now.day % 3 == 0 and time_now.hour == 0 and time_now.minute == 0:
                progress = int((time_now - self.time_start) /
                               (self.time_end - self.time_start) * 100)
                print(self.map_name+':'+str(progress).rjust(3, ' ')+'%完了しました')
        video.release()
        print(self.map_name+':100%完了しました')


class Map_run(threading.Thread):
    def __init__(self, map_name, interval, day_list, save_path, fps):
        threading.Thread.__init__(self)
        self.A = Map(map_name, interval, day_list, save_path, fps)

    def run(self):
        self.A.make_video()
