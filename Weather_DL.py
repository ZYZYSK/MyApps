from Weather import *
from concurrent import futures
import datetime
import time as tm


def jma_downloader():
    print('___JMA Downloader___')
    # ファイルの保存場所とダウンロード開始日時の情報を取得
    JMA_dl.get_settings()
    # ファイルの保存場所に移動
    JMA_dl.move_path()
    # ジョブリスト
    job_list = []

    # クラスの指定　
    infrared = JMA_dl('infrared', 'https://www.jma.go.jp/jp/gms/imgs_c/0/infrared/1/', 10)
    infrared_earth = JMA_dl('infrared_earth', 'https://www.jma.go.jp/jp/gms/imgs_c/6/infrared/1/', 10)
    radar = JMA_dl('radar', 'https://www.jma.go.jp/jp/radnowc/imgs/radar/000/', 5)
    visible = JMA_dl('visible', 'https://www.jma.go.jp/jp/gms/imgs_c/0/visible/1/', 10)
    visible_earth = JMA_dl('visible_earth', 'https://www.jma.go.jp/jp/gms/imgs_c/6/visible/1/', 10)
    watervapor = JMA_dl('watervapor', 'https://www.jma.go.jp/jp/gms/imgs_c/0/watervapor/1/', 10)
    watervapor_earth = JMA_dl('watervapor_earth', 'https://www.jma.go.jp/jp/gms/imgs_c/6/watervapor/1/', 10)
    weather_map = JMA_dl_weathermap('weather_map', 'https://www.jma.go.jp/jp/g3/images/jp_c/', 180)

    # クラスリスト
    jma_list = [infrared, infrared_earth, radar, visible,
                visible_earth, watervapor, watervapor_earth, weather_map]
    # ダウンロード
    with futures.ProcessPoolExecutor(max_workers=len(jma_list)) as executor:
        for i in jma_list:
            job_list.append(executor.submit(i.download_map))
        _ = futures.as_completed(fs=job_list)


def gpv_downloader():
    print('___GPV Downloader___')
    # ファイルの保存場所とダウンロード開始日時の情報を取得
    GPV_dl.get_settings()
    # ファイルの保存場所に移動
    GPV_dl.move_path()
    # フォルダを作成
    GPV_dl.make_dirs()
    # grib2ファイルをダウンロード
    GPV_dl.download_grib2()
    # ジョブリスト
    job_list = []
    # クラスリスト
    gpv_list = []
    # 開始日時
    time = datetime.datetime(GPV_dl.time_start.year, GPV_dl.time_start.month, GPV_dl.time_start.day, 00, 00)
    print("開始日時: {0}".format(time))
    with futures.ProcessPoolExecutor(max_workers=12) as executor:
        # 実行
        while time.date() < GPV_dl.time_end:
            job_list.append(executor.submit(exec_gpv, time=time, gpv_list=gpv_list))
            time += datetime.timedelta(hours=6)
        _ = futures.as_completed(fs=job_list)
    # 設定ファイルの更新
    GPV_dl.update_settings()
    # 一時ファイルの削除
    for i in gpv_list:
        del i
        tm.sleep(1)
    # GPV_dl.rm_tmp()
    GPV_dl.exit_program('正常に完了しました')


def exec_gpv(time, gpv_list):
    gpv_cls = GPV_dl(time)
    gpv_list.append(gpv_cls)
    gpv_cls.j_300_hw()
    gpv_cls.j_500_ht()
    gpv_cls.j_500_hv()
    gpv_cls.j_500_t_700_dewp()
    gpv_cls.j_850_ht()
    gpv_cls.j_850_tw_700_vv()
    gpv_cls.j_850_eptw()


if __name__ == "__main__":
    jma_downloader()
    gpv_downloader()
