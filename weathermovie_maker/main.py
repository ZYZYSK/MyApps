# 気象衛星画像から動画を作成するプログラム
import shutil
import os
import re
import datetime
from func import *


def main():
    maptype = ['image', 'infrared', 'infrared_earth', 'radar', 'visible',
               'visible_earth', 'watervapor', 'watervapor_earth']  # 対象となるフォルダ名
    mapname = move_path(maptype)  # 画像の種類
    # print(path)
    datelist = assign_date(mapname)  # 開始日と終了日
    # print(datelist)
    print('fps(radarは24,それ以外は12がデフォルト)：', end='')
    frame = float(input())
    # print(frame)
    path = save_path()  # 保存先の指定
    # print(path)
    if mapname == 'radar':
        make_video(mapname, datelist[0], datelist[1], 5, frame, path)
    else:
        make_video(mapname, datelist[0], datelist[1], 10, frame, path)


if __name__ == "__main__":
    main()
