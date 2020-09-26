# 気象衛星画像から動画を作成するプログラム
from concurrent import futures
from maker import *


def make_jma():
    # 保存場所に移動
    JMA_Maker.move_path()
    # 開始日時と終了日時を入力
    JMA_Maker.assign_time()
    # 保存先の指定
    JMA_Maker.save_path()
    # 一括作成するかどうか
    JMA_Maker.lump()
    # 一括作成する場合
    if JMA_Maker.islump == True:
        for map_name in JMA_Maker.map_list:
            # 画像間隔の設定
            interval = 5 if map_name == 'radar' else 180 if map_name == 'weather_map' else 10
            # fpsの設定
            fps = 24 if map_name == 'radar' else 2.0 / 3.0 if map_name == 'weather_map' else 12
            # 実行準備
            map_cls = JMA_Maker(map_name, interval, fps)
            # 実行
            map_cls.make_video()
    else:
        # 作成する画像の種類を決定
        map_name = JMA_Maker.get_map_name()
        # 画像間隔の設定
        interval = 5 if map_name == 'radar' else 180 if map_name == 'weather_map' else 10
        # 実行準備
        map_cls = JMA_Maker(map_name, interval, JMA_Maker.get_fps(map_name))
        # 実行
        map_cls.make_video()
    JMA_Maker.exit_program('正常に完了しました')


if __name__ == "__main__":
    make_jma()
