import os
import datetime
import shutil
from time import sleep
from python_modules import file_open
from python_modules import file_download


def get_image():
    file_open.open_file('weather_setting.txt')
    os.makedirs('infrared', exist_ok=True)
    os.makedirs('infrared_earth', exist_ok=True)
    os.makedirs('radar', exist_ok=True)
    os.makedirs('radar_kyusu', exist_ok=True)
    os.makedirs('visible', exist_ok=True)
    os.makedirs('visible_earth', exist_ok=True)
    os.makedirs('watervapor', exist_ok=True)
    os.makedirs('watervapor_earth', exist_ok=True)
    # 開始時刻を設定
    a = datetime.datetime.now() - datetime.timedelta(days=5)
    base = list(a.strftime("%Y%m%d%H%M"))
    n = int(base[-1])
    base[-1] = '0'
    base = ''.join(base)
    # 現在時刻
    b = datetime.datetime.now() - datetime.timedelta(minutes=10)
    time = list(b.strftime("%Y%m%d%H%M"))
    m = int(time[-1])
    time[-1] = '0'
    time = ''.join(time)
    os.chdir('infrared')
    m_download(
        base, time, 'https://www.jma.go.jp/jp/gms/imgs_c/0/infrared/1/', 'infrared')
    os.chdir('../infrared_earth')
    m_download(
        base, time, 'https://www.jma.go.jp/jp/gms/imgs_c/6/infrared/1/', 'infrared_earth')
    os.chdir('../radar')
    m_download(
        base, time, 'https://www.jma.go.jp/jp/radnowc/imgs/radar/000/', 'radar')
    os.chdir('../radar_kyusu')
    m_download(
        base, time, 'https://www.jma.go.jp/jp/radnowc/imgs/radar/214/', 'radar_kyusu')
    os.chdir('../visible')
    m_download(
        base, time, 'https://www.jma.go.jp/jp/gms/imgs_c/0/visible/1/', 'visible')
    os.chdir('../visible_earth')
    m_download(
        base, time, 'https://www.jma.go.jp/jp/gms/imgs_c/6/visible/1/', 'visible_earth')
    os.chdir('../watervapor')
    m_download(
        base, time, 'https://www.jma.go.jp/jp/gms/imgs_c/0/watervapor/1/', 'watervapor')
    os.chdir('../watervapor_earth')
    m_download(
        base, time, 'https://www.jma.go.jp/jp/gms/imgs_c/6/watervapor/1/', 'watervapor_earth')


def m_download(base, time, url_base, image_type):
    while os.path.isfile(image_type + '_' + base + '.png') == True:
        base = base_plus(base, image_type)
    while int(base) <= int(time):
        url = url_base + base + '-00.png'
        image_name = image_type + '_' + base + '.png'
        # インターネット接続確認
        if file_download.check_url('https://www.jma.go.jp/jma/index.html') == True:
            if file_download.check_url(url) == True:  # ダウンロードしたいファイルが存在するか
                # ダウンロード失敗
                if file_download.download_file(url, image_name) == False:
                    continue
                else:  # ダウンロード成功
                    print('ダウンロード中...')
            else:  # ダウンロードしたいファイルが存在しない
                try:  # 前時間のファイルからコピーする
                    if image_type == 'radar':  # レーダーの場合
                        shutil.copy(image_type + '_' + (datetime.datetime.strptime(base, '%Y%m%d%H%M') - datetime.timedelta(
                            minutes=5)).strftime('%Y%m%d%H%M') + '.png', image_type + '_' + base + '.png')
                    else:  # それ以外
                        shutil.copy(image_type + '_' + (datetime.datetime.strptime(base, '%Y%m%d%H%M') - datetime.timedelta(
                            minutes=10)).strftime('%Y%m%d%H%M') + '.png', image_type + '_' + base + '.png')
                except FileNotFoundError:  # 前時間のファイルも存在しない
                    pass
            base = base_plus(base, image_type)  # 時間を進める
        else:
            print('インターネット未接続...')
            sleep(10)


def base_plus(base, image_type):
    if image_type == 'radar':
        basetime = datetime.datetime.strptime(
            base, '%Y%m%d%H%M') + datetime.timedelta(minutes=5)
    else:
        basetime = datetime.datetime.strptime(
            base, '%Y%m%d%H%M') + datetime.timedelta(minutes=10)
    base = basetime.strftime('%Y%m%d%H%M')
    return base


if __name__ == "__main__":
    get_image()
