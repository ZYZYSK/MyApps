import os


def get_location(file_name):  # 画像の保存場所を設定したファイルを読み出す
    try:
        file_stream = open(file_name, mode='r')
    except Exception:
        file_stream = open(file_name, mode='w')
        file_stream.write('.')
    finally:
        location = file_stream.readline()
        file_stream.close()
        # print(location)
        return location


def location_chdir(location):  # 画像の保存場所に移動
    try:
        os.makedirs(location, exist_ok=True)
        os.chdir(location)
        # print(os.getcwd())
    except FileNotFoundError:
        print('指定されたパスは存在しません。location.txtを正しく設定してください。')
