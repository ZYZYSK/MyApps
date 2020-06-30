import os
import re
import datetime
import numpy as np
import cv2


def move_path(maptype):
    while True:
        print('移動先(current：カレントディレクトリ)：')
        path = input()
        if path == 'current':
            path = os.getcwd()
        try:
            os.chdir(path)
        except FileNotFoundError:
            print("移動先が見つかりません")
        else:
            lastpath = re.search('[\w:\\\\]*\\\\(\w*)', path)
            # print(lastpath.group(1))
            if lastpath.group(1) in maptype:
                break
    return lastpath.group(1)


def assign_date(mapname):
    while True:
        print("開始日と終了日を入力してください(入力形式：yyyy/mm/dd):")
        start = input().replace('/', '')
        end = input().replace('/', '')
        start = mapname + '_' + start + '0000.png'
        end = mapname + '_' + end
        end = end + ('2355.png' if mapname == 'radar' else '2350.png')
        starttime = datetime.datetime.strptime(
            start, mapname + '_%Y%m%d%H%M.png')
        endtime = datetime.datetime.strptime(
            end, mapname + '_%Y%m%d%H%M.png')
        # print(starttime.strftime('%Y/%m/%d/%H/%M') +
        #       ' '+endtime.strftime('%Y/%m/%d/%H/%M'))
        # print(start + ' ' + end)
        if os.path.isfile(start) and os.path.isfile(end) and endtime >= starttime:
            break
    return starttime, endtime


def save_path():
    while True:
        print('保存先(current：カレントディレクトリ)：')
        path = input()
        if path == 'current':
            path = os.getcwd()
        try:
            os.makedirs(path, exist_ok=True)
        except FileNotFoundError:
            print("保存先が見つかりません")
        else:
            break
    return path


def make_video(mapname, STARTTIME, ENDTIME, count, frame, path):
    # print(STARTTIME.strftime('%Y/%m/%d/%H/%M') +
    #       ' ' + ENDTIME.strftime('%Y/%m/%d/%H/%M'))
    ctime = STARTTIME  # 最初の時間
    NAME = mapname + '_' + \
        STARTTIME.strftime('%Y%m%d%H%M') + '.png'  # 先頭のファイル名
    IMG = cv2.imread(NAME, 1)  # 先頭のファイルを開く
    HEIGHT = IMG.shape[0]  # 解像度のy
    WIDTH = IMG.shape[1]  # 解像度のx
    VNAME = os.path.join(path, mapname + '.mp4')  # ビデオ名
    if os.path.isfile(VNAME):
        while True:
            print('同じファイルが存在しますが上書きしますか？(y/n)：', end='')
            t = input()
            if t == 'y':
                break
            elif t == 'n':
                exit()
    print('名前：'+VNAME+', 解像度：' + str(WIDTH) + 'X' +
          str(HEIGHT) + ', fps：'+str(frame))
    fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
    video = cv2.VideoWriter(VNAME, fourcc, frame, (WIDTH, HEIGHT))
    while (ctime <= ENDTIME):
        cname = mapname+'_'+ctime.strftime('%Y%m%d%H%M')+'.png'  # /ファイル名
        # print(cname)
        cimg = cv2.imread(cname, 1)
        ctime = ctime + datetime.timedelta(minutes=count)
        if (cimg is None) or (cimg.shape[0] != HEIGHT) or (cimg.shape[1] != WIDTH):
            continue
        video.write(cimg)
        if ctime.day % 3 == 0 and ctime.hour == 0 and ctime.minute == 0:
            progress = int((ctime - STARTTIME) / (ENDTIME - STARTTIME) * 100)
            print(str(progress).rjust(3, ' ')+'%完了しました')
    video.release()
    print('100%完了しました')
