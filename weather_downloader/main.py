from gpv import *
from jma import *
from concurrent import futures
import datetime
import time as tm


def jma_downloader():
    print('___JMA Downloader___')
    # ファイルの保存場所とダウンロード開始日時の情報を取得
    JMA.get_settings()
    # ファイルの保存場所に移動
    JMA.move_path()
    # ジョブリスト
    job_list = []
    # クラスリスト
    infrared = JMA('infrared', 'https://www.jma.go.jp/jp/gms/imgs_c/0/infrared/1/', 10)
    infrared_earth = JMA('infrared_earth', 'https://www.jma.go.jp/jp/gms/imgs_c/6/infrared/1/', 10)
    radar = JMA('radar', 'https://www.jma.go.jp/jp/radnowc/imgs/radar/000/', 5)
    visible = JMA('visible', 'https://www.jma.go.jp/jp/gms/imgs_c/0/visible/1/', 10)
    visible_earth = JMA('visible_earth', 'https://www.jma.go.jp/jp/gms/imgs_c/6/visible/1/', 10)
    watervapor = JMA('watervapor', 'https://www.jma.go.jp/jp/gms/imgs_c/0/watervapor/1/', 10)
    watervapor_earth = JMA('watervapor_earth', 'https://www.jma.go.jp/jp/gms/imgs_c/6/watervapor/1/', 10)
    weather_map = JMA_weathermap('weather_map', 'https://www.jma.go.jp/jp/g3/images/jp_c/', 180)
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
    GPV.get_settings()
    # ファイルの保存場所に移動
    GPV.move_path()
    # フォルダを作成
    GPV.make_dirs()
    # grib2ファイルをダウンロード
    GPV.download_grib2()
    # ジョブリスト
    job_list = []
    # クラスリスト
    gpv_list = []
    # 開始日時
    time = datetime.datetime(GPV.time_start.year, GPV.time_start.month, GPV.time_start.day, 00, 00)
    with futures.ProcessPoolExecutor(max_workers=20) as executor:
        # 実行
        while time.date() < GPV.time_end:
            job_list.append(executor.submit(exec_gpv, time=time, gpv_list=gpv_list))
            time += datetime.timedelta(hours=6)
        _ = futures.as_completed(fs=job_list)
    # 設定ファイルの更新
    GPV.update_settings()
    # 一時ファイルの削除
    for i in gpv_list:
        del i
        tm.sleep(1)
    # GPV.rm_tmp()
    GPV.exit_program('正常に完了しました')


def exec_gpv(time, gpv_list):
    gpv_cls = GPV(time)
    gpv_list.append(gpv_cls)
    gpv_cls.j_300_hw()
    gpv_cls.j_500_ht()
    gpv_cls.j_500_hv()
    gpv_cls.j_500_t_700_dewp()
    gpv_cls.j_850_ht()
    gpv_cls.j_850_tw_700_vv()
    gpv_cls.j_850_eptw()


if __name__ == '__main__':
    jma_downloader()
    gpv_downloader()
