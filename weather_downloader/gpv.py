import os
import shutil
import datetime
import time as tm
import sys
import requests
from concurrent import futures
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from matplotlib import cm
from matplotlib.colors import ListedColormap
from metpy.units import units
import metpy.calc as mpcalc
import numpy as np
from scipy.ndimage import gaussian_filter
import pygrib as grib


class GPV:
    # 設定ファイルの場所
    settings_file_path = os.path.join(os.path.dirname(__file__), 'gpv_settings.txt')
    # 何日前から
    days_duration = 7
    # 保存場所
    path = None
    # ダウンロード開始日時
    time_start = None
    # ダウンロード終了日時
    time_end = None
    # 時差
    time_diff = 9
    # 範囲(日本域)
    lat_min_jp = 0
    lat_max_jp = 70
    lon_min_jp = 60
    lon_max_jp = 200
    extent_jp = [100, 170, 10, 60]
    # ランベルト正角円錐図法(日本域)
    mapcrs_jp = ccrs.LambertConformal(
        central_longitude=140, central_latitude=35, standard_parallels=(30, 60))
    # 正距円筒図法
    datacrs = ccrs.PlateCarree()
    @classmethod
    def exit_program(cls, e, info=None):  # プログラムの終了
        if not info is None:
            exc_type, exc_obj, exc_tb = info
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno, '行目')
        print(e)
        print('\'q\'で終了します')
        while True:
            s = input()
            if s == 'q':
                sys.exit()

    @classmethod
    def get_settings(cls):    # データの保存場所とダウンロード開始日時の情報を取得
        try:
            f = open(cls.settings_file_path, 'r')
        except FileNotFoundError:
            f = open(cls.settings_file_path, 'w')
            f.write('.')
            f.close()
            f = open(cls.settings_file_path, 'r')
        except Exception as e:
            cls.exit_program(e, sys.exc_info())
        finally:
            settings = [i.strip('\n') for i in f.readlines()]
            path = settings[0]
            if len(settings) > 1:
                try:
                    time_start = datetime.datetime.strptime(
                        settings[1], '%Y/%m/%d')
                except Exception as e:
                    cls.exit_program(e, sys.exc_info())
            else:
                time_start = datetime.date.today() - datetime.timedelta(days=cls.days_duration)
            print('保存先：' + path, 'ダウンロード開始日時：' + time_start.strftime('%Y/%m/%d'))
            cls.path = path
            cls.time_start = time_start
            f.close()

    @classmethod
    def move_path(cls):    # データの保存場所に移動
        try:
            os.makedirs(cls.path, exist_ok=True)
            os.chdir(cls.path)
            print(os.getcwd())
        except FileNotFoundError:
            cls.exit_program('指定されたパスは正しくありません. gpv_settings.txtを正しく設定してください.')
        except Exception as e:
            cls.exit_program(e, sys.exc_info())

    @classmethod
    def download_grib2_2(cls, time):
        file_name = os.path.join('tmp', time.strftime('%Y%m%d%H'))
        if os.path.exists(file_name):
            return
        # urlの作成
        url_a = 'http://database.rish.kyoto-u.ac.jp/arch/jmadata/data/gpv/original/' + \
            time.strftime('%Y/%m/%d/')
        url_b = 'Z__C_RJTD_' + \
            time.strftime('%Y%m%d%H%M%S') + '_GSM_GPV_Rgl_FD0000_grib2.bin'
        url = url_a + url_b
        # ダウンロード
        while True:
            # ダウンロード試行
            try:
                req = requests.get(url, timeout=10)
            # ダウンロードできない場合
            except Exception as e:
                print(e)
                tm.sleep(10)
            # ダウンロードが成功したらファイルを保存
            else:
                print('[ダウンロード] ' + file_name)
                with open(file_name, 'wb') as fp:
                    fp.write(req.content)
                break

    @classmethod
    def download_grib2(cls):  # grib2ファイルをダウンロード
        # ダウンロード開始日時
        time = datetime.datetime(cls.time_start.year, cls.time_start.month, cls.time_start.day, 00, 00)
        # ダウンロード終了日時の次の日
        cls.time_end = datetime.date.today() - datetime.timedelta(days=1)
        # ジョブリスト
        job_list = []
        with futures.ProcessPoolExecutor(max_workers=5) as executor:
            while time.date() < cls.time_end:
                job_list.append(executor.submit(cls.download_grib2_2, time=time))
                # 日時を進める
                time += datetime.timedelta(hours=6)
            _ = futures.as_completed(fs=job_list)

    @classmethod
    def update_settings(cls):  # 設定ファイルのダウンロード開始日時の情報を更新
        with open(cls.settings_file_path, mode='w') as f:
            f.write(cls.path + '\n')
            f.write(cls.time_end.strftime('%Y/%m/%d'))
        print('設定ファイルの情報を更新しました')

    @classmethod
    def rm_tmp(cls):  # 一時ファイルを削除
        try:
            shutil.rmtree(os.path.join(cls.path, 'tmp'))
        except Exception as e:
            cls.exit_program(e, sys.exc_info())

    @classmethod
    def make_dirs(cls):  # フォルダを作成
        dir_list = ['tmp', 'j300hw', 'j500ht', 'j500hv', 'j500t700td', 'j850ht', 'j850tw700vv', 'j850eptw']
        for dirs in dir_list:
            os.makedirs(dirs, exist_ok=True)

    @classmethod
    def set_ax_jp(cls):  # 地図(日本域)を作成
        # 地図
        ax_jp = plt.subplot(111, projection=cls.mapcrs_jp)
        # 地図の範囲を設定
        ax_jp.set_extent(cls.extent_jp, cls.datacrs)
        # 海岸線を追加
        ax_jp.add_feature(cfeature.COASTLINE.with_scale('50m'))
        # 国境線を追加
        ax_jp.add_feature(cfeature.BORDERS.with_scale('50m'))
        # 陸の塗りつぶし
        ax_jp.add_feature(cfeature.LAND, color='black', alpha=0.8)
        # 格子線の大きさ、色、線種、間隔の設定(ここでは緯線と経線をひく)
        ax_jp.gridlines(xlocs=mticker.MultipleLocator(10),
                        ylocs=mticker.MultipleLocator(10),
                        linestyle=':', color='grey')
        return ax_jp

    @classmethod
    def gpv_select_jp(cls, gpv, shortName, level):  # 指定したデータを取得(日本域)
        return gpv.select(shortName=shortName, level=level)[0].data(lat1=cls.lat_min_jp, lat2=cls.lat_max_jp, lon1=cls.lon_min_jp, lon2=cls.lon_max_jp)

    @classmethod
    def colorbar_jp(cls, cf):  # カラーバー
        return plt.colorbar(cf, orientation='horizontal', fraction=0.05, shrink=0.95, aspect=100, pad=0)

    def __init__(self, time_now):
        # grib2ファイル名
        self.gpv_path = os.path.join('tmp', time_now.strftime('%Y%m%d%H'))
        # ファイルを開く
        self.gpv = grib.open(self.gpv_path)
        # 時刻
        self.time_str1 = (time_now + datetime.timedelta(hours=self.time_diff)).strftime('%Y%m%d%H')
        self.time_str2 = (time_now + datetime.timedelta(hours=self.time_diff)).strftime('%Y/%m/%d/%H')

    def __del__(self):
        self.gpv.close()

    def j_300_hw(self):  # 300hPa Height & Winds in Japan
        # 300hPa高度、緯度、経度の取得
        height, lat, lon = self.gpv_select_jp(self.gpv, 'gh', 300)
        height = gaussian_filter(height, sigma=3.0)
        # 300hPa風の取得
        uwnd, _, _ = self.gpv_select_jp(self.gpv, 'u', 300) * units('m/s')
        vwnd, _, _ = self.gpv_select_jp(self.gpv, 'v', 300) * units('m/s')
        sped = mpcalc.wind_speed(uwnd, vwnd).to('kt')
        # 図の数、大きさを設定
        fig = plt.figure(1, figsize=(294 / 25.4, 210 / 25.4))
        # 地図の描画
        ax = self.set_ax_jp()
        # 等風速線を引く
        cf = ax.contourf(lon, lat, sped, np.arange(0, 220, 20), extend='max', cmap='YlGnBu', transform=self.datacrs, alpha=0.9)
        # 風ベクトルの表示
        wind_slice = (slice(None, None, 10), slice(None, None, 10))
        ax.barbs(lon[wind_slice], lat[wind_slice], uwnd[wind_slice].to('kt').m, vwnd[wind_slice].to('kt').m, pivot='middle', color='black', alpha=0.5, transform=self.datacrs)
        # 等高度線を引く
        cs = ax.contour(lon, lat, height, np.arange(5400, 12000, 120), colors='black', transform=self.datacrs)
        plt.clabel(cs, fmt='%d')
        # カラーバーをつける
        cbar = self.colorbar_jp(cf)
        cbar.set_label('Isotach (kt)')
        # タイトルをつける
        plt.title('300hpa: HEIGHT (m), WIND ARROW (kt), ISOTACH (kt)', loc='left')
        plt.title(self.time_str2, loc='right')
        # 大きさの調整
        plt.subplots_adjust(bottom=0.1, top=0.9)
        # 保存
        print('[' + self.time_str2 + '] 300hPa高度、風 を作成中...')
        plt.savefig(os.path.join('j300hw', 'j300hw_' + self.time_str1 + '.png'))
        # 閉じる
        plt.close(fig=fig)

    def j_500_ht(self):  # 500hPa Height & Temperture in Japan
        # 500hPa高度、緯度、経度の取得
        height, lat, lon = self.gpv_select_jp(self.gpv, 'gh', 500)
        height = gaussian_filter(height, sigma=3.0)
        # 500hPa気温の取得
        temp, _, _ = self.gpv_select_jp(self.gpv, 't', 500)
        temp = (temp * units.kelvin).to(units.celsius)
        # 図の数、大きさを設定
        fig = plt.figure(1, figsize=(294 / 25.4, 210 / 25.4))
        # 地図の描画
        ax = self.set_ax_jp()
        # 等温線を引く
        clevs_temp = np.arange(-48, 9, 3)
        cf = ax.contourf(lon, lat, temp, clevs_temp, extend='both', cmap='jet', transform=self.datacrs, alpha=0.9)
        cg = ax.contour(lon, lat, temp, clevs_temp, colors='black', linestyles='dashed', alpha=0.5, transform=self.datacrs)
        plt.clabel(cg, levels=np.arange(-48, 9, 6), colors='black', fontsize=10, rightside_up=False, fmt='%d')
        # 等高度線を引く
        cs = ax.contour(lon, lat, height, np.arange(0, 8000, 60), colors='black', transform=self.datacrs)
        plt.clabel(cs, levels=np.hstack((np.arange(0, 5700, 120), np.arange(5700, 6000, 60))), fmt='%d')
        # カラーバーをつける
        cbar = self.colorbar_jp(cf)
        cbar.set_label('Temperature ($^\circ$C)')
        # タイトルをつける
        plt.title('500hPa: HEIGHT (M), TEMP ($^\circ$C)', loc='left')
        plt.title(self.time_str2, loc='right')
        # 大きさの調整
        plt.subplots_adjust(bottom=0.1, top=0.9)
        # 保存
        print('[' + self.time_str2 + '] 500hPa高度、気温 を作成中...')
        plt.savefig(os.path.join('j500ht', 'j500ht_' + self.time_str1 + '.png'))
        # 閉じる
        plt.close(fig=fig)

    def j_500_hv(self):  # 500hPa Height & Vorticity & Winds in Japan
        # 500hPa高度、緯度、経度の取得
        height, lat, lon = self.gpv_select_jp(self.gpv, 'gh', 500)
        height = gaussian_filter(height, sigma=3.0)
        # 500hPa風の取得
        uwnd, _, _ = self.gpv_select_jp(self.gpv, 'u', 500) * units('m/s')
        vwnd, _, _ = self.gpv_select_jp(self.gpv, 'v', 500) * units('m/s')
        # 渦度の計算
        dx, dy = mpcalc.lat_lon_grid_deltas(lon, lat)
        avor = mpcalc.vorticity(uwnd, vwnd, dx, dy, dim_order='yx')
        # 図の数、大きさを設定
        fig = plt.figure(1, figsize=(294 / 25.4, 210 / 25.4))
        # 地図の描画
        ax = self.set_ax_jp()
        # カラーマップを作成する
        N = 140
        M = 380
        PuBu = np.flipud(cm.get_cmap('BuPu', N)(range(N)))
        YlOrRd = cm.get_cmap('YlOrRd', M)(range(M))
        PuBuYlOrRd = ListedColormap(np.vstack((PuBu, YlOrRd)))
        # 等渦度線を引く
        clevs_vort = np.arange(-120, 380, 20)
        cf = ax.contourf(lon, lat, avor * 10**6, clevs_vort, extend='both', cmap=PuBuYlOrRd, transform=self.datacrs, alpha=0.9)
        # 風ベクトルの表示
        wind_slice = (slice(None, None, 10), slice(None, None, 10))
        ax.barbs(lon[wind_slice], lat[wind_slice], uwnd[wind_slice].to('kt').m, vwnd[wind_slice].to('kt').m, pivot='middle', color='black', alpha=0.5, transform=self.datacrs)
        # 等高度線を引く
        clevs_hght = np.arange(0, 8000, 60)
        cs = ax.contour(lon, lat, height, clevs_hght, colors='black', transform=self.datacrs)
        plt.clabel(cs, levels=np.hstack((np.arange(0, 5700, 120), np.arange(5700, 6000, 60))), fmt='%d')
        # カラーバーをつける
        cbar = self.colorbar_jp(cf)
        cbar.set_label('Vorticity ($10^{-6}/s$)')
        # タイトルをつける
        plt.title('500hPa: HEIGHT (M), VORT ($10^{-6}/s$), WIND ARROW (kt)', loc='left')
        plt.title(self.time_str2, loc='right')
        # 大きさの調整
        plt.subplots_adjust(bottom=0.1, top=0.9)
        # 保存
        print('[' + self.time_str2 + '] 500hPa高度、渦度、風 を作成中...')
        plt.savefig(os.path.join('j500hv', 'j500hv_' + self.time_str1 + '.png'))
        # 閉じる
        plt.close(fig=fig)

    def j_500_t_700_dewp(self):  # 500hPa Temperature & 700hPa Dew point depression
        # 500hPa気温、緯度、経度の取得
        temp, lat, lon = self.gpv_select_jp(self.gpv, 't', 500)
        temp = (temp * units.kelvin).to(units.celsius)
        # 700hPa湿数の取得
        temp_700, _, _ = self.gpv_select_jp(self.gpv, 't', 700) * units.kelvin
        rh, _, _ = self.gpv_select_jp(self.gpv, 'r', 700)
        rh *= 0.01
        dewp_700 = mpcalc.dewpoint_from_relative_humidity(temp_700, rh)
        td = temp_700 - dewp_700
        # 図の数、大きさを設定
        fig = plt.figure(1, figsize=(294 / 25.4, 210 / 25.4))
        # 地図の描画
        ax = self.set_ax_jp()
        # カラーマップを作成する
        N = 256
        M_PuBu = np.flipud(cm.get_cmap('BuPu', N)(range(N)))
        PuBu = ListedColormap(M_PuBu)
        # 等湿数線を引く
        clevs_td = np.arange(0, 21, 1)
        cf = ax.contourf(lon, lat, td, clevs_td, extend='both', cmap=PuBu, transform=self.datacrs, alpha=0.9)
        clevs_td2 = np.array([-100, 3])
        cg = ax.contour(lon, lat, td, clevs_td2, colors='yellow', linestyles='solid', transform=self.datacrs)
        # 等温線を引く
        clevs_temp = np.arange(-60, 30, 3)
        cs = ax.contour(lon, lat, temp, clevs_temp, colors='black', linestyles='solid', transform=self.datacrs)
        plt.clabel(cs, fmt='%d')
        # カラーバーをつける
        cbar = self.colorbar_jp(cf)
        cbar.set_label('T-Td ($^\circ$C)')
        # タイトルをつける
        plt.title('500hPa: TEMP ($^\circ$C)\n700hPa: T-TD ($^\circ$C)', loc='left')
        plt.title(self.time_str2, loc='right')
        # 大きさの調整
        plt.subplots_adjust(bottom=0.1, top=0.9)
        # 保存
        print('[' + self.time_str2 + '] 500hPa気温、700hPa湿数 を作成中...')
        plt.savefig(os.path.join('j500t700td', 'j500t700td_' + self.time_str1 + '.png'))
        # 閉じる
        plt.close(fig=fig)

    def j_850_ht(self):  # 850hPa Height & Temperture in Japan
        # 850hPa高度、緯度、経度の取得
        height, lat, lon = self.gpv_select_jp(self.gpv, 'gh', 850)
        height = gaussian_filter(height, sigma=3.0)
        # 850hPa気温の取得
        temp, _, _ = self.gpv_select_jp(self.gpv, 't', 850)
        temp = (temp * units.kelvin).to(units.celsius)
        # 図の数、大きさを設定
        fig = plt.figure(1, figsize=(294 / 25.4, 210 / 25.4))
        # 地図の描画
        ax = self.set_ax_jp()
        # 等温線を引く
        clevs_temp = np.arange(-24, 33, 3)
        cf = ax.contourf(lon, lat, temp, clevs_temp, extend='both', cmap='jet', transform=self.datacrs, alpha=0.9)
        cg = ax.contour(lon, lat, temp, clevs_temp, colors='black', linestyles='dashed', alpha=0.5, transform=self.datacrs)
        plt.clabel(cg, levels=np.arange(-24, 33, 6), colors='black', fontsize=10, rightside_up=False, fmt='%d')
        # 等高度線を引く
        cs = ax.contour(lon, lat, height, np.arange(0, 8000, 60), colors='black', transform=self.datacrs)
        plt.clabel(cs, fmt='%d')
        # カラーバーをつける
        cbar = self.colorbar_jp(cf)
        cbar.set_label('Temperature ($^\circ$C)')
        # タイトルをつける
        plt.title('850hPa: HEIGHT (M), TEMP ($^\circ$C)', loc='left')
        plt.title(self.time_str2, loc='right')
        # 大きさの調整
        plt.subplots_adjust(bottom=0.1, top=0.9)
        # 保存
        print('[' + self.time_str2 + '] 850hPa高度、気温 を作成中...')
        plt.savefig(os.path.join('j850ht', 'j850ht_' + self.time_str1 + '.png'))
        # 閉じる
        plt.close(fig=fig)

    def j_850_tw_700_vv(self):  # 850hPa Temperture, Wind & 700hPa Vertical Velocity in Japan
        # 850hPa気温、緯度、経度の取得
        temp, lat, lon = self.gpv_select_jp(self.gpv, 't', 850)
        temp = (gaussian_filter(temp, sigma=1.0) * units.kelvin).to(units.celsius)
        # 700hPa上昇流の取得
        vv, _, _ = self.gpv_select_jp(self.gpv, 'w', 700)
        vv = (vv * units.Pa / units.second).to(units.hPa / units.hour)
        # 850hPa風の取得
        uwnd, _, _ = self.gpv_select_jp(self.gpv, 'u', 850) * units('m/s')
        vwnd, _, _ = self.gpv_select_jp(self.gpv, 'v', 850) * units('m/s')
        # 図の数、大きさを設定
        fig = plt.figure(1, figsize=(294 / 25.4, 210 / 25.4))
        # 地図の描画
        ax = self.set_ax_jp()
        # カラーマップを作成する
        N = 125
        M = 65
        RdOrYl = np.flipud(cm.get_cmap('YlOrRd', N)(range(N)))
        BuPu = cm.get_cmap('BuPu', M)(range(M))
        RdOrYlBuPu = ListedColormap(np.vstack((RdOrYl, BuPu)))
        # 等上昇流線を引く
        cf = ax.contourf(lon, lat, vv, np.arange(-120, 65, 5), extend='both', cmap=RdOrYlBuPu, transform=self.datacrs, alpha=0.9)
        # 風ベクトルの表示
        wind_slice = (slice(None, None, 10), slice(None, None, 10))
        ax.barbs(lon[wind_slice], lat[wind_slice], uwnd[wind_slice].to('kt').m, vwnd[wind_slice].to('kt').m, pivot='middle', color='black', alpha=0.5, transform=self.datacrs)
        # 等温線を引く
        cs = ax.contour(lon, lat, temp, np.arange(-60, 60, 3), colors='black', transform=self.datacrs)
        plt.clabel(cs, levels=np.arange(-60, 60, 6), fmt='%d')
        # カラーバーをつける
        cbar = self.colorbar_jp(cf)
        cbar.set_label('Vertial Velocity (hPa/h)')
        # タイトルをつける
        plt.title('850hPa: HEIGHT (M), WIND ARROW (kt)\n700hPa: VERTICAL VELOCITY (hPa/h)', loc='left')
        plt.title(self.time_str2, loc='right')
        # 大きさの調整
        plt.subplots_adjust(bottom=0.1, top=0.9)
        # 保存
        print('[' + self.time_str2 + '] 850hPa気温、風、700hPa鉛直流 を作成中...')
        plt.savefig(os.path.join('j850tw700vv', 'j850tw700vv_' + self.time_str1 + '.png'))
        # 閉じる
        plt.close(fig=fig)

    def j_850_eptw(self):  # 850hPa Equivalent Potential Temperture & Wind in Japan
        # 850hPa気温の取得
        temp, lat, lon = self.gpv_select_jp(self.gpv, 't', 850)
        temp = temp * units.kelvin
        # 850hPa風の取得
        uwnd, _, _ = self.gpv_select_jp(self.gpv, 'u', 850) * units('m/s')
        vwnd, _, _ = self.gpv_select_jp(self.gpv, 'v', 850) * units('m/s')
        # 850hPa相対湿度の取得
        rh, _, _ = self.gpv_select_jp(self.gpv, 'r', 850)
        rh *= 0.01
        # 露点温度の計算
        dewp = mpcalc.dewpoint_from_relative_humidity(temp, rh)
        # 相当温位の計算
        ept = mpcalc.equivalent_potential_temperature(850 * units.hPa, temp, dewp)
        ept = gaussian_filter(ept, sigma=1.0)
        # 図の数、大きさを設定
        fig = plt.figure(1, figsize=(294 / 25.4, 210 / 25.4))
        # 地図の描画
        ax = self.set_ax_jp()
        # 等温線を引く
        clevs_ept = np.arange(255, 372, 3)
        cf = ax.contourf(lon, lat, ept, clevs_ept, extend='both', cmap='jet', transform=self.datacrs, alpha=0.9)
        cg = ax.contour(lon, lat, ept, clevs_ept, colors='black', linestyles='solid', linewidths=1, transform=self.datacrs)
        plt.clabel(cg, levels=np.arange(258, 372, 6), fmt='%d')
        # 風ベクトルの表示
        wind_slice = (slice(None, None, 3), slice(None, None, 3))
        ax.barbs(lon[wind_slice], lat[wind_slice], uwnd[wind_slice].to('kt').m,
                 vwnd[wind_slice].to('kt').m, pivot='middle', length=4, color='black', alpha=0.5, transform=self.datacrs)
        # カラーバーをつける
        cbar = self.colorbar_jp(cf)
        cbar.set_label('E.P.TEMP (K)')
        # タイトルをつける
        plt.title('850hPa: E.P.TEMP (K), WIND ARROW (kt)', loc='left')
        plt.title(self.time_str2, loc='right')
        # 大きさの調整
        plt.subplots_adjust(bottom=0.1, top=0.9)
        # 保存
        print('[' + self.time_str2 + '] 850hPa相当温位、風 を作成中...')
        plt.savefig(os.path.join('j850eptw', 'j850eptw_' + self.time_str1 + '.png'))
        # 閉じる
        plt.close(fig=fig)
