from func import *
from gpvclass import *
import datetime  # tmp


def main():
    # # ファイルの保存場所とダウンロード開始日時の情報を取得
    # location, time_start = get_settings('settings.txt')
    # # ファイルの保存場所に移動
    # move_location(location)
    # # grib2ファイルをダウンロード
    # time_end = download_grib2(time_start)
    # # 設定ファイルの更新
    # update_settings('settings.txt', location, time_end)
    # 試験
    a = GPV('.', datetime.datetime(2020, 9, 5, 12))
    # a.j_300_hw()
    # a.j_500_ht()
    # a.j_500_hv()
    # a.j_850_ht()
    # a.j_850_tw_700_vv()
    a.j_850_eptw()


if __name__ == '__main__':
    main()
