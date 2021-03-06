import os
import sys
import datetime
import signal
from tkinter import filedialog
import tkinter as tk

import cv2

from ..functions import exit_program, handler_sigint


def jma_maker():
    # SIGINTシグナルを受け取る
    signal.signal(signal.SIGINT, handler_sigint)
    # 保存場所に移動
    JmaMaker.move_path()
    # 開始日時と終了日時を入力
    JmaMaker.assign_time()
    # 保存先の指定
    JmaMaker.save_path()
    # 一括作成するかどうか
    JmaMaker.lump()
    # 作成を続けるかどうか
    is_continue = True
    # 一括作成する場合
    if JmaMaker.islump == True:
        for map_name in JmaMaker.map_list:
            # 画像間隔の設定
            interval = 5 if map_name == 'radar' else 180 if map_name == 'weather_map' else 10
            # fpsの設定
            fps = 24 if map_name == 'radar' else 2.0 / 3.0 if map_name == 'weather_map' else 12
            # 実行準備
            map_cls = JmaMaker(map_name, interval, fps)
            # 実行
            map_cls.make_video()
    else:
        while is_continue:
            # 作成する画像の種類を決定
            map_name = JmaMaker.get_map_name()
            # 画像間隔の設定
            interval = 5 if map_name == 'radar' else 180 if map_name == 'weather_map' else 10
            # 実行準備
            map_cls = JmaMaker(map_name, interval)
            # 実行
            map_cls.make_video()
            # 実行を続けるか
            while True:
                print("続けて動画を作成しますか？(y/n): ", end='')
                s = input()
                if s == "n":
                    is_continue = False
                    break
                elif s == "y":
                    break
    exit_program('正常に完了しました')


class JmaMaker:
    # 対象となる画像の種類
    map_list = ['infrared', 'infrared_earth', 'radar', 'visible', 'visible_earth', 'watervapor', 'watervapor_earth', 'weather_map']
    # 開始時刻
    time_start = None
    # 終了時刻
    time_end = None
    # 保存先のパス
    path = None
    # 一括作成するかどうか
    islump = False

    @classmethod
    def move_path(cls):  # 画像の保存場所に移動
        while True:
            root = tk.Tk()
            root.withdraw()
            path = filedialog.askdirectory(title="JMA画像の保存場所...", initialdir=os.path.dirname(__file__))
            root.destroy()
            try:
                os.chdir(path)
            except Exception as e:
                exit_program(e, sys.exc_info())
            else:
                ismaplist = True  # 移動先が正しいかどうか
                for maptype in cls.map_list:
                    if os.path.isdir(maptype) == False:  # 移動先が正しくない
                        print("移動先が正しくありません")
                        ismaplist = False
                        break
                if ismaplist:  # 移動先が正しい場合
                    print("{0} に移動しました".format(os.getcwd()))
                    break

    @classmethod
    def assign_time(cls):  # 開始日時と終了日時を入力
        print("開始日時と終了日時を入力してください(入力形式:yyyy/mm/dd/hh/MM):")
        cls.time_start = datetime.datetime.strptime(input().replace('/', ''), '%Y%m%d%H%M')
        cls.time_end = datetime.datetime.strptime(input().replace('/', ''), '%Y%m%d%H%M')

    @classmethod
    def save_path(cls):  # 保存先の指定
        while True:
            root = tk.Tk()
            root.withdraw()
            cls.path = filedialog.askdirectory(title="動画の保存先...", initialdir=os.path.dirname(__file__))
            root.destroy()
            if cls.path == '':
                exit_program("キャンセルされました")
            else:
                print(cls.path + 'に保存します')
                break

    @classmethod
    def lump(cls):  # 一括作成するかどうか
        while True:
            print("一括作成しますか(y/n):", end='')
            s = input().lower()
            if s == 'y' or s == 'n':
                if s == 'y': cls.islump = True; break
                if s == 'n': break

    @classmethod
    def get_map_name(cls):  # 作成する画像の種類を決定
        while True:
            print("作成する画像の種類:", end='')
            s = input().lower()
            if s in cls.map_list:
                print(s + "を作成します")
                return s

    def get_fps(self):  # 何fpsで動画を作成するか入力する
        while True:
            print(self.map_name + ':fps(radarは24,それ以外は12):', end='')
            try:
                fps = float(input())
            except Exception:
                pass
            else:
                self.fps = fps
                break

    def __init__(self, map_name, interval, fps=0):
        # 画像の種類
        self.map_name = map_name
        # 日時の間隔
        self.interval = interval
        # fps
        self.fps = fps
        if fps == 0:
            self.get_fps()

    def make_video(self):  # 動画作成
        if self.interval <= 60:
            time_now = datetime.datetime(self.time_start.year, self.time_start.month, self.time_start.day, self.time_start.hour, (self.time_start.minute // self.interval) * self.interval)
        else:
            time_now = datetime.datetime(self.time_start.year, self.time_start.month, self.time_start.day, (self.time_start.hour // (self.interval // 60)) * (self.interval // 60), 00)
        # 先頭のファイル名
        if self.map_name == 'weather_map':
            file_name = os.path.join(self.map_name, self.map_name + '_' +
                                     self.time_start.strftime('%Y%m%d%H')[2:] + '.png')
        else:
            file_name = os.path.join(self.map_name, self.map_name + '_' +
                                     self.time_start.strftime('%Y%m%d%H%M') + '.png')
        # 先頭のファイルを開く
        img = cv2.imread(file_name, 1)
        if img is None:
            exit_program(img + ':ファイルが存在しません')
        # 解像度のy
        height = img.shape[0]
        # 解像度のx
        width = img.shape[1]
        # ビデオ名
        video_name = os.path.join(self.path, self.map_name + '.mp4')
        # 同じ名前のビデオが存在する場合
        if os.path.isfile(video_name):
            while True:
                print(self.map_name + ':同じファイルが存在しますが上書きしますか？(y/n):')
                s = input().lower()
                if s == 'y':
                    break
                elif s == 'n':
                    exit_program('プログラムを終了します')
        # ビデオ情報を表示
        print('名前:' + video_name + ', 解像度:' + str(width) + 'X' + str(height) + ', fps:' + str(self.fps))
        # mp4形式で作成
        fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
        # ビデオ情報を設定
        video = cv2.VideoWriter(video_name, fourcc, self.fps, (width, height))
        # ビデオ作成
        while (time_now <= self.time_end):
            # ファイル名の設定
            if self.map_name == 'weather_map':
                cname = os.path.join(self.map_name, self.map_name + '_' + time_now.strftime('%Y%m%d%H')[2:] + '.png')
            else:
                cname = os.path.join(self.map_name, self.map_name + '_' + time_now.strftime('%Y%m%d%H%M') + '.png')
            # 画像を開く
            cimg = cv2.imread(cname, 1)
            # 日時を進める
            time_now += datetime.timedelta(minutes=self.interval)
            # 画像を開けない場合や、画像が正しくない場合
            if (cimg is None) or (cimg.shape[0] != height) or (cimg.shape[1] != width):
                print(cname + ':ファイルが存在しないか、正しくありません')
                continue
            # 画像をビデオに書き込む
            video.write(cimg)
            # 進歩率を表示
            if time_now.day % 3 == 0 and time_now.hour == 0 and time_now.minute == 0:
                progress = int((time_now - self.time_start) /
                               (self.time_end - self.time_start) * 100)
                print(self.map_name + ':' + str(progress).rjust(3, ' ') + '%完了しました')
        # ビデオを閉じる
        video.release()
        print(self.map_name + ':100%完了しました')
