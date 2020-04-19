# 指定したパス下のpng画像から動画を作るプログラム
import os
import cv2
import numpy as np
import glob


def make_movie():
    print('指定したパス下のフォルダ名だけをコピーするプログラムです。')
    input_path()
    png_list = []
    for x in glob.glob('*.png'):
        png_list.append(x)
    while True:
        start = (int)(search_img(png_list, '開始時刻を入力してください：(例：202006231450)'))
        if start != -1:
            break
    while True:
        end = (int)(search_img(png_list, '終了時刻を入力してください：(例：202006231450)'))
        if end != -1:
            break
    while True:
        interval = (int)(set_interval())
        if interval > 0:
            break
    for x in range(start, end):
        pass


def input_path():
    while True:
        print('コピー元のパスを入力してください：')
        m_path = input('>>')
        try:
            os.chdir(m_path)
        except:
            pass
        else:
            break


def search_img(png_list, message):
    print(message)
    start = input('>>')
    for x in png_list:
        if start in x == True:
            return png_list.index(x)
    return -1


def set_interval():
    print('一枚の継続時間：')
    interval = input('>>')
    return interval
