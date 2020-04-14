import os
import requests
import urllib
import datetime
import shutil


def get_image():
    try:
        f = open('weather_setting.txt', mode='r')
        folderpath = f.readline()
        os.chdir(folderpath)
    except FileNotFoundError:
        f = open('weather_setting.txt', mode='x')
    finally:
        f.close()
        os.makedirs('infrared', exist_ok=True)
        os.makedirs('infrared_earth', exist_ok=True)
        os.makedirs('radar', exist_ok=True)
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


def m_download(base, time, url_base, m_type):
    while (os.path.isfile(m_type + '_' + base + '.png') == True):
        if m_type == 'radar':
            basetime = datetime.datetime.strptime(
                base, '%Y%m%d%H%M') + datetime.timedelta(minutes=5)
        else:
            basetime = datetime.datetime.strptime(
                base, '%Y%m%d%H%M') + datetime.timedelta(minutes=10)
        base = basetime.strftime('%Y%m%d%H%M')
    while (int(base) <= int(time)):
        url = url_base + base + '-00.png'
        try:
            f = urllib.request.urlopen(url)
            f.close()
            req = requests.get(url)
            with open(m_type + '_' + base + '.png', "wb") as w:
                w.write(req.content)
                w.close()
        except (ConnectionError, ConnectionAbortedError, ConnectionRefusedError, ConnectionResetError):
            pass

        except urllib.request.HTTPError:
            if m_type == 'radar':
                try:
                    shutil.copy(m_type + '_' + (datetime.datetime.strptime(base, '%Y%m%d%H%M') -
                                                datetime.timedelta(minutes=5)).strftime('%Y%m%d%H%M') + '.png', m_type + '_' + base + '.png')
                except FileNotFoundError:
                    pass
                finally:
                    basetime = datetime.datetime.strptime(
                        base, '%Y%m%d%H%M') + datetime.timedelta(minutes=5)

            else:
                try:
                    shutil.copy(m_type + '_' + (datetime.datetime.strptime(base, '%Y%m%d%H%M') -
                                                datetime.timedelta(minutes=10)).strftime('%Y%m%d%H%M') + '.png', m_type + '_' + base + '.png')
                except FileNotFoundError:
                    pass
                finally:
                    basetime = datetime.datetime.strptime(
                        base, '%Y%m%d%H%M') + datetime.timedelta(minutes=10)
            base = basetime.strftime('%Y%m%d%H%M')

        else:
            if m_type == 'radar':
                basetime = datetime.datetime.strptime(
                    base, '%Y%m%d%H%M') + datetime.timedelta(minutes=5)
            else:
                basetime = datetime.datetime.strptime(
                    base, '%Y%m%d%H%M') + datetime.timedelta(minutes=10)
            base = basetime.strftime('%Y%m%d%H%M')


get_image()
