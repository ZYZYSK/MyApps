from func1 import *
from mapclass import *


def main():
    location = get_location('location.txt')  # ファイルの保存場所が書かれたファイルを開く
    move_location(location)  # ファイルの保存場所に移動
    infrared = Map_default_run(
        'infrared', 'https://www.jma.go.jp/jp/gms/imgs_c/0/infrared/1/', Map_default, 10)
    infrared_earth = Map_default_run(
        'infrared_earth', 'https://www.jma.go.jp/jp/gms/imgs_c/0/infrared/1/', Map_default, 10)
    radar = Map_default_run(
        'radar', 'https://www.jma.go.jp/jp/radnowc/imgs/radar/000/', Map_default, 5)
    visible = Map_default_run(
        'visible', 'https://www.jma.go.jp/jp/gms/imgs_c/0/visible/1/', Map_default, 10)
    visible_earth = Map_default_run(
        'visible_earth', 'https://www.jma.go.jp/jp/gms/imgs_c/6/visible/1/', Map_default, 10)
    watervapor = Map_default_run(
        'watervapor', 'https://www.jma.go.jp/jp/gms/imgs_c/0/watervapor/1/', Map_default, 10)
    watervapor_earth = Map_default_run(
        'watervapor_earth', 'https://www.jma.go.jp/jp/gms/imgs_c/6/watervapor/1/', Map_default, 10)
    map_list = [infrared, infrared_earth, radar, visible,
                visible_earth, watervapor, watervapor_earth]
    for i in map_list:
        i.start()


if __name__ == '__main__':
    main()
