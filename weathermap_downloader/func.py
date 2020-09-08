import os
import sys
import urllib
import time


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


def get_location(file_name):  # 画像の保存場所を設定したファイルを読み出す
    try:
        file_stream = open(file_name, mode='r')
    except FileNotFoundError:
        file_stream = open(file_name, mode='w')
        file_stream.write('.')
    except Exception as e:
        exit_program(e,sys.exc_info)
    finally:
        location = file_stream.readline()
        file_stream.close()
        # print(location)
        return location


def move_location(location):  # 画像の保存場所に移動
    try:
        os.makedirs(location, exist_ok=True)
        os.chdir(location)
        print(os.getcwd())
    except FileNotFoundError:
        exit_program('指定されたパスは存在しません. location.txtを正しく設定してください.')
    except Exception as e:
        exit_program(e,sys.exc_info)


def check_connection():  # ネット接続が確立されるまで待機
    while True:
        try:
            urllib.request.urlopen(
                'https://www.jma.go.jp/jma/index.html')  # ネット接続を確認
        except Exception:
            print('インターネットに接続できません')
            time.sleep(10)
        else:
            break


def check_is_on_server(url):  # ダウンロードするファイルがサーバーに存在するか確認
    try:
        urllib.request.urlopen(url)
    except Exception:
        return False
    else:
        return True
