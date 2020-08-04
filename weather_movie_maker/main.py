# 気象衛星画像から動画を作成するプログラム
from func import *
from mapclass import *


def main():
    map_list = ['infrared', 'infrared_earth', 'radar', 'visible',
                'visible_earth', 'watervapor', 'watervapor_earth']  # 対象となるフォルダ名
    move_location(map_list)  # 画像の保存場所に移動
    day_list = assign_date()  # 開始日と終了日を入力
    save_path = save_location()  # 保存先の指定
    if lump():  # 一括作成する場合
        for map_name in map_list:  # 開始日と終了日をチェック
            check_date(map_name, day_list)
            interval = 5 if map_name == 'radar'else 10
            fps = 24 if map_name == 'radar' else 12
            job = Map_run(map_name, interval, day_list,
                          save_path, fps)
            job.start()
    else:
        map_name = get_map_name(map_list)  # 作成する画像の種類を決定
        check_date(map_name, day_list)  # 開始日と終了日をチェック
        interval = 5 if map_name == 'radar' else 10
        job = Map_run(map_name, interval, day_list,
                      save_path, get_fps(map_name))
        job.start()
    job.join()
    exit_program('正常に完了しました')


if __name__ == "__main__":
    main()
