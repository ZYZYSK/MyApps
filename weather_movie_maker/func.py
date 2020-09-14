import os
import sys
import urllib
import time
import datetime


def exit_program(e, info=None):  # プログラムを終了させる
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


def move_location(map_list):  # 画像の保存場所に移動
    while True:
        print('移動先(current:カレントディレクトリ):', end='')
        path = input()
        if path == 'current':
            path = os.getcwd()
        try:
            os.chdir(path)
        except FileNotFoundError:
            print("移動先が見つかりません")
        except Exception as e:
            exit_program(e, sys.exc_info())
        else:
            ismaplist = True  # 移動先が正しいかどうか
            for maptype in map_list:
                if os.path.isdir(maptype) == False:  # 移動先が正しくない
                    print("移動先が正しくありません")
                    ismaplist = False
                    break
            if ismaplist:  # 移動先が正しい場合
                print(os.getcwd()+"に移動しました")
                break


def assign_time():  # 開始日時と終了日時を入力
    print("開始日時と終了日時を入力してください(入力形式:yyyy/mm/dd/hh/MM):")
    start_time = input().replace('/', '')
    end_time = input().replace('/', '')
    return start_time, end_time


def lump():  # 一括作成するかどうか
    while True:
        print("一括作成しますか(y/n):", end='')
        s = input().lower()
        if s == 'y' or s == 'n':
            return True if s == 'y' else False


def check_time(map_name, time_list):  # 開始日時と終了日時をチェック
    if map_name == 'weather_map':
        return
    map_start = map_name + '_' + time_list[0] + '.png'
    map_end = map_name + '_' + time_list[1] + '.png'
    try:
        time_start = datetime.datetime.strptime(
            map_start, map_name + '_%Y%m%d%H%M.png')
        time_end = datetime.datetime.strptime(
            map_end, map_name + '_%Y%m%d%H%M.png')
    except Exception:
        exit_program(map_name + ":開始日時と終了日時が正しくありません")
    if not (os.path.isfile(os.path.join(map_name, map_start)) and time_end >= time_start):
        exit_program(map_name + ":開始日時と終了日時が正しくありません")


def get_map_name(map_list):  # 作成する画像の種類を決定
    while True:
        print("作成する画像の種類:", end='')
        s = input().lower()
        if s in map_list:
            print(s+"を作成します")
            return s


def save_location():  # 保存先の指定
    while True:
        print('保存先(current:カレントディレクトリ):', end='')
        path = input()
        if path == 'current':
            path = os.getcwd()
        try:
            os.makedirs(path, exist_ok=True)
        except FileNotFoundError:
            print("保存先が正しくありません")
        except Exception as e:
            exit_program(e, sys.exc_info())
        else:
            print(path+'に保存します')
            return path


def get_fps(map_name):  # 何fpsで動画を作成するか入力する
    while True:
        print(map_name+':fps(radarは24,それ以外は12):', end='')
        try:
            fps = float(input())
        except Exception:
            pass
        else:
            return fps
