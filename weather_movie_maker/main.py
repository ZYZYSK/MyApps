# 気象衛星画像から動画を作成するプログラム
from func import *
from mapclass import *


def main():
    # 対象となる画像の種類
    map_list = ['infrared', 'infrared_earth', 'radar', 'visible',
                'visible_earth', 'watervapor', 'watervapor_earth', 'weather_map']
    # 画像の保存場所に移動
    move_location(map_list)
    # 開始日時と終了日時を入力
    time_list = assign_time()
    # 保存先の指定
    save_path = save_location()
    # ジョブリスト
    job_list = []
    # 一括作成する場合
    if lump():
        for map_name in map_list:
            # 開始日時と終了日時をチェック
            check_time(map_name, time_list)
            # 画像間隔の設定
            interval = 5 if map_name == 'radar' else 180 if map_name == 'weather_map' else 10
            # fpsの設定
            fps = 24 if map_name == 'radar' else 2.0 / \
                3.0 if map_name == 'weather_map' else 12
            # 実行準備
            job = Map_run(map_name, interval, time_list,
                          save_path, fps)
            # 実行
            job.start()
            # ジョブリストに追加
            job_list.append(job)
    else:
        # 作成する画像の種類を決定
        map_name = get_map_name(map_list)
        # 開始日時と終了日時をチェック
        check_time(map_name, time_list)
        # 画像間隔の設定
        interval = 5 if map_name == 'radar' else 180 if map_name == 'weather_map' else 10
        # 実行準備

        job = Map_run(map_name, interval, time_list,
                      save_path, get_fps(map_name))
        # 実行
        job.start()
        # ジョブリストに追加
        job_list.append(job)
    # 実行終了を待つ
    for job in job_list:
        job.join()
    exit_program('正常に完了しました')


if __name__ == "__main__":
    main()
