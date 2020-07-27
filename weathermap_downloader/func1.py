import os
import sys
import urllib
import time


def exit_program(e):
    print(e)
    print("エラーが発生したので終了します.")
    sys.exit()


def get_location(file_name):  # 画像の保存場所を設定したファイルを読み出す
    try:
        file_stream = open(file_name, mode='r')
    except FileNotFoundError:
        file_stream = open(file_name, mode='w')
        file_stream.write('.')
    except Exception as e:
        exit_program(e)
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
        print('指定されたパスは存在しません. location.txtを正しく設定してください.')
    except Exception as e:
        exit_program(e)


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
