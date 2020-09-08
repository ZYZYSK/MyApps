import os
import sys
import datetime

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


def get_settings(file_name):
    try:
        f = open(file_name, 'r')
    except FileNotFoundError:
        f = open(file_name, 'w')
        f.write('.')
        f.close()
        f = open(file_name, 'r')
    except Exception as e:
        exit_program(sys.exc_info, e)
    finally:
        settings = [i.strip('\n') for i in f.readlines()]
        location = settings[0]
        if len(settings) > 1:
            try:
                time_start = datetime.datetime.strptime(
                    settings[1], '%Y/%m/%d')
            except Exception as e:
                exit_program(sys.exc_info, e)
        else:
            time_start = datetime.date().today()-datetime.timedelta(days=DAYS_DURATION)
        print('保存先：'+location, 'ダウンロード開始日時：' +
              datetime.date.strftime('%Y/%m/%d'))
        return location, time_start


def move_location(location):
    try:
        os.makedirs(location, exist_ok=True)
    except Exception as e:
        exit_program(sys.exc_info(), e)
