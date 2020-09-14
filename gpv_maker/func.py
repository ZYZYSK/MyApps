import os
import sys
import datetime
import requests
import time as tm
import threading
DAYS_DURATION = 6


def exit_program(e, info=None):
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


def get_settings(file_name):    # ファイルの保存場所とダウンロード開始日時の情報を取得
    try:
        f = open(file_name, 'r')
    except FileNotFoundError:
        f = open(file_name, 'w')
        f.write('.')
        f.close()
        f = open(file_name, 'r')
    except Exception as e:
        exit_program(e, sys.exc_info())
    finally:
        settings = [i.strip('\n') for i in f.readlines()]
        location = settings[0]
        if len(settings) > 1:
            try:
                time_start = datetime.datetime.strptime(
                    settings[1], '%Y/%m/%d')
            except Exception as e:
                exit_program(e, sys.exc_info())
        else:
            time_start = datetime.date.today()-datetime.timedelta(days=DAYS_DURATION)
        print('保存先：'+location, 'ダウンロード開始日時：' +
              time_start.strftime('%Y/%m/%d'))
        return location, time_start


def update_settings(file_name, location, time_end):  # 設定ファイルのダウンロード開始日時の情報を更新
    file_name = os.path.join(os.path.dirname(__file__), file_name)
    with open(file_name, mode='w') as f:
        f.write(location + '\n')
        f.write(time_end.strftime('%Y/%m/%d'))
    print('設定情報を更新しました')


def move_location(location):    # ファイルの保存場所に移動
    try:
        os.makedirs(location, exist_ok=True)
        os.chdir(location)
        print(os.getcwd())
    except FileNotFoundError:
        exit_program('指定されたパスは存在しません. settings.txtを正しく設定してください.')
    except Exception as e:
        exit_program(e, sys.exc_info())


def download_grib2(time_start):  # grib2ファイルをダウンロード
    # ダウンロード開始日時
    time = datetime.datetime(
        time_start.year, time_start.month, time_start.day, 00, 00)
    # ダウンロード終了日時の次の日
    time_end = datetime.date.today()
    # urlの取得
    while time.date() < time_end:
        # urlの作成
        # http://database.rish.kyoto-u.ac.jp/arch/jmadata/data/gpv/original/2020/09/05/Z__C_RJTD_20200905000000_GSM_GPV_Rgl_FD0000_grib2.bin
        url_a = 'http://database.rish.kyoto-u.ac.jp/arch/jmadata/data/gpv/original/' + \
            time.strftime('%Y/%m/%d/')
        url_b = 'Z__C_RJTD_' + \
            time.strftime('%Y%m%d%H%M%S')+'_GSM_GPV_Rgl_FD0000_grib2.bin'
        url = url_a+url_b
        print('[ダウンロード]', url)
        # ダウンロード
        while True:
            # ダウンロード試行
            try:
                req = requests.get(url, timeout=10)
            # ダウンロードできない場合
            except Exception as e:
                print(e)
                tm.sleep(10)
            # ダウンロードが成功したらファイルを保存
            else:
                file_name = os.path.join('tmp', time.strftime('%Y%m%d%H'))
                os.makedirs('tmp', exist_ok=True)
                with open(file_name, 'wb') as fp:
                    fp.write(req.content)
                break
        # 日時を進める
        time += datetime.timedelta(hours=6)
    return time_end
