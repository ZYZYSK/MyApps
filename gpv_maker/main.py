from func import *
from gpvclass import *


def main():
    # ファイルの保存場所とダウンロード開始日時の情報を取得
    location, time_start = get_settings('settings.txt')
    # ファイルの保存場所に移動
    move_location(location)
    # grib2ファイルをダウンロード
    time_end = download_grib2(time_start)
    # 設定ファイルの更新
    update_settings('settings.txt', location, time_end)
    # 試験
    a = GPV(location, time_start)
    a.hpa_500_jp()


if __name__ == '__main__':
    main()
