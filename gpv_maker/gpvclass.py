from func import *
import os
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
    # ランベルト正角円錐図法(日本域)
    mapcrs_jp = ccrs.LambertConformal(
        central_longitude=140, central_latitude=35, standard_parallels=(30, 60))
    # 正距円筒図法
    datacrs = ccrs.PlateCarree()
    @classmethod
    def set_ax_jp(cls):  # 地図(日本域)を作成
        # 地図
        ax_jp = plt.subplot(111, projection=cls.mapcrs_jp)
        # 地図の範囲を設定
        ax_jp.set_extent([100, 170, 10, 60], cls.datacrs)
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

    def __init__(self, location, time_now):
        # grib2ファイル名
        self.gpv_path = os.path.join('tmp', time_now.strftime('%Y%m%d%H'))
        # ファイルを開く
        self.gpv = grib.open(self.gpv_path)
        # 時刻
        self.time_str1 = time_now.strftime('%Y%m%d%H')
        self.time_str2 = time_now.strftime('%Y/%m/%d/%H')
        # フォルダを作成
        jmap = ['j300hw', 'j500ht', 'j500hv', 'j850ht', 'j850tw700vv', 'j850eptw']
        [os.makedirs(i, exist_ok=True) for i in jmap]

    def j_300_hw(self):  # 300hPa Height & Winds in Japan
        # 300hPa高度、緯度、経度の取得
        height, lat, lon = self.gpv.select(shortName='gh', level=300)[0].data()
        height = gaussian_filter(height, sigma=3.0)
        # 300hPa風の取得
        uwnd, _, _ = self.gpv.select(shortName='u', level=300)[0].data() * units('m/s')
        vwnd, _, _ = self.gpv.select(shortName='v', level=300)[0].data() * units('m/s')
        sped = mpcalc.wind_speed(uwnd, vwnd).to('kt')
        # 図の数、大きさを設定
        fig = plt.figure(1, figsize=(294 / 25.4, 210 / 25.4))
        # 地図の描画
        ax = self.set_ax_jp()
        # 20ktごとに200ktまで等風速線を引く
        clevs_sped = np.arange(0, 220, 20)
        cf = ax.contourf(lon, lat, sped, clevs_sped, extend='max', cmap='YlGnBu', transform=self.datacrs, alpha=0.9)
        # 風ベクトルの表示
        wind_slice = (slice(None, None, 10), slice(None, None, 10))
        ax.barbs(lon[wind_slice], lat[wind_slice], uwnd[wind_slice].to('kt').m, vwnd[wind_slice].to('kt').m, pivot='middle', color='black', alpha=0.5, transform=self.datacrs)
        # 120mごとに12000mまで等高度線を引く
        clevs_hght = np.arange(5400, 12000, 120)
        cs = ax.contour(lon, lat, height, clevs_hght, colors='black', transform=self.datacrs)
        plt.clabel(cs, fmt='%d')
        # カラーバーをつける
        cbar = plt.colorbar(cf, orientation='horizontal', fraction=0.05, shrink=0.95, aspect=100, pad=0)
        cbar.set_label('Isotach (kt)')
        # タイトルをつける
        plt.title('300hpa: HEIGHT (m), WIND ARROW (kt), ISOTACH (kt)', loc='left')
        plt.title(self.time_str2, loc='right')
        # 大きさの調整
        plt.subplots_adjust(bottom=0.1, top=0.9)
        # 保存
        plt.savefig(os.path.join('j300hw', 'j300hw_' + self.time_str1 + '.png'))
        # 閉じる
        plt.close(fig=fig)

    def j_500_ht(self):  # 500hPa Height & Temperture in Japan
        # 500hPa高度、緯度、経度の取得
        height, lat, lon = self.gpv.select(shortName='gh', level=500)[0].data()
        height = gaussian_filter(height, sigma=3.0)
        # 500hPa気温の取得
        temp, _, _ = self.gpv.select(shortName='t', level=500)[0].data()
        temp = (temp * units.kelvin).to(units.celsius)
        # 図の数、大きさを設定
        fig = plt.figure(1, figsize=(294 / 25.4, 210 / 25.4))
        # 地図の描画
        ax = self.set_ax_jp()
        # 3℃ごとに15℃まで等温線を引く
        clevs_temp = np.arange(-60, 15, 3)
        cf = ax.contourf(lon, lat, temp, clevs_temp, extend='both', cmap='jet', transform=self.datacrs, alpha=0.9)
        cg = ax.contour(lon, lat, temp, clevs_temp, colors='black', linestyles='dashed', alpha=0.5, transform=self.datacrs)
        plt.clabel(cg, fmt='%d')
        # 60mごとに8000mまで等高度線を引く
        clevs_hght = np.arange(0, 8000, 60)
        cs = ax.contour(lon, lat, height, clevs_hght, colors='black', transform=self.datacrs)
        plt.clabel(cs, fmt='%d')
        # カラーバーをつける
        cbar = plt.colorbar(cf, orientation='horizontal', fraction=0.05, shrink=0.95, aspect=100, pad=0)
        cbar.set_label('Temperature ($^\circ$C)')
        # タイトルをつける
        plt.title('500hPa: HEIGHT (M), TEMP ($^\circ$C)', loc='left')
        plt.title(self.time_str2, loc='right')
        # 大きさの調整
        plt.subplots_adjust(bottom=0.1, top=0.9)
        # 保存
        plt.savefig(os.path.join('j500ht', 'j500ht_' + self.time_str1 + '.png'))
        # 閉じる
        plt.close(fig=fig)

    def j_500_hv(self):  # 500hPa Height & Vorticity & Winds in Japan
        # 500hPa高度、緯度、経度の取得
        height, lat, lon = self.gpv.select(shortName='gh', level=500)[0].data()
        height = gaussian_filter(height, sigma=3.0)
        # 500hPa風の取得
        uwnd, _, _ = self.gpv.select(shortName='u', level=500)[0].data() * units('m/s')
        vwnd, _, _ = self.gpv.select(shortName='v', level=500)[0].data() * units('m/s')
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
        # 60mごとに8000mまで等高度線を引く
        clevs_hght = np.arange(0, 8000, 60)
        cs = ax.contour(lon, lat, height, clevs_hght, colors='black', transform=self.datacrs)
        plt.clabel(cs, fmt='%d')
        # カラーバーをつける
        cbar = plt.colorbar(cf, orientation='horizontal', fraction=0.05, shrink=0.95, aspect=100, pad=0)
        cbar.set_label('Vorticity ($10^{-6}/s$)')
        # タイトルをつける
        plt.title('500hPa: HEIGHT (M), VORT ($10^{-6}/s$), WIND ARROW (kt)', loc='left')
        plt.title(self.time_str2, loc='right')
        # 大きさの調整
        plt.subplots_adjust(bottom=0.1, top=0.9)
        # 保存
        plt.savefig(os.path.join('j500hv', 'j500hv_' + self.time_str1 + '.png'))
        # 閉じる
        plt.close(fig=fig)

    def j_850_ht(self):  # 850hPa Height & Temperture in Japan
        # 850hPa高度、緯度、経度の取得
        height, lat, lon = self.gpv.select(shortName='gh', level=850)[0].data()
        height = gaussian_filter(height, sigma=3.0)
        # 850hPa気温の取得
        temp, _, _ = self.gpv.select(shortName='t', level=850)[0].data()
        temp = (temp * units.kelvin).to(units.celsius)
        # 図の数、大きさを設定
        fig = plt.figure(1, figsize=(294 / 25.4, 210 / 25.4))
        # 地図の描画
        ax = self.set_ax_jp()
        # 3℃ごとに15℃まで等温線を引く
        clevs_temp = np.arange(-18, 33, 3)
        cf = ax.contourf(lon, lat, temp, clevs_temp, extend='both', cmap='jet', transform=self.datacrs, alpha=0.9)
        cg = ax.contour(lon, lat, temp, clevs_temp, colors='black', linestyles='dashed', alpha=0.5, transform=self.datacrs)
        plt.clabel(cg, fmt='%d')
        # 60mごとに8000mまで等高度線を引く
        clevs_hght = np.arange(0, 8000, 60)
        cs = ax.contour(lon, lat, height, clevs_hght, colors='black', transform=self.datacrs)
        plt.clabel(cs, fmt='%d')
        # カラーバーをつける
        cbar = plt.colorbar(cf, orientation='horizontal', fraction=0.05, shrink=0.95, aspect=100, pad=0)
        cbar.set_label('Temperature ($^\circ$C)')
        # タイトルをつける
        plt.title('850hPa: HEIGHT (M), TEMP ($^\circ$C)', loc='left')
        plt.title(self.time_str2, loc='right')
        # 大きさの調整
        plt.subplots_adjust(bottom=0.1, top=0.9)
        # 保存
        plt.savefig(os.path.join('j850ht', 'j850ht_' + self.time_str1 + '.png'))
        # 閉じる
        plt.close(fig=fig)

    def j_850_tw_700_vv(self):  # 850hPa Temperture, Wind & 700hPa Vertical Velocity in Japan
        # 850hPa気温、緯度、経度の取得
        temp, lat, lon = self.gpv.select(shortName='t', level=850)[0].data()
        temp = (gaussian_filter(temp, sigma=3.0) * units.kelvin).to(units.celsius)
        # 700hPa上昇流の取得
        vv, _, _ = self.gpv.select(shortName='w', level=700)[0].data()
        vv = (vv * units.Pa / units.second).to(units.hPa / units.hour)
        # 850hPa風の取得
        uwnd, _, _ = self.gpv.select(shortName='u', level=850)[0].data() * units('m/s')
        vwnd, _, _ = self.gpv.select(shortName='v', level=850)[0].data() * units('m/s')
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
        clevs_vv = np.arange(-120, 65, 5)
        cf = ax.contourf(lon, lat, vv, clevs_vv, extend='both', cmap=RdOrYlBuPu, transform=self.datacrs, alpha=0.9)
        # 風ベクトルの表示
        wind_slice = (slice(None, None, 10), slice(None, None, 10))
        ax.barbs(lon[wind_slice], lat[wind_slice], uwnd[wind_slice].to('kt').m, vwnd[wind_slice].to('kt').m, pivot='middle', color='black', alpha=0.5, transform=self.datacrs)
        # 等温線を引く
        clevs_temp = np.arange(-60, 60, 3)
        cs = ax.contour(lon, lat, temp, clevs_temp, colors='black', transform=self.datacrs)
        plt.clabel(cs, fmt='%d')
        # カラーバーをつける
        cbar = plt.colorbar(cf, orientation='horizontal', fraction=0.05, shrink=0.95, aspect=100, pad=0)
        cbar.set_label('Vertial Velocity (hPa/h)')
        # タイトルをつける
        plt.title('850hPa: HEIGHT (M), WIND ARROW (kt)\n700hPa: VERTICAL VELOCITY (hPa/h)', loc='left')
        plt.title(self.time_str2, loc='right')
        # 大きさの調整
        plt.subplots_adjust(bottom=0.1, top=0.9)
        # 保存
        plt.savefig(os.path.join('j850tw700vv', 'j850tw700vv_' + self.time_str1 + '.png'))
        # 閉じる
        plt.close(fig=fig)

    def j_850_eptw(self):  # 850hPa Equivalent Potential Temperture & Wind in Japan
        [print(self.gpv.message(i)) for i in range(1, 50)]
        # 気圧、緯度、経度の取得
        pres, lat, lon = self.gpv.select(shortName='prmsl', level=0)[0].data()
        pres = pres * units.Pa
        # 850hPa気温の取得
        temp, _, _ = self.gpv.select(shortName='t', level=1000)[0].data()
        temp = temp * units.kelvin
        # 850hPa風の取得
        uwnd, _, _ = self.gpv.select(shortName='u', level=850)[0].data() * units('m/s')
        vwnd, _, _ = self.gpv.select(shortName='v', level=850)[0].data() * units('m/s')
        # 850hPa相対湿度の取得
        rh, _, _ = self.gpv.select(shortName='r', level=1000)[0].data()
        rh *= 0.01
        # 露点温度の計算
        dewp = mpcalc.dewpoint_from_relative_humidity(temp, rh)
        # 相当温位の計算
        ept = mpcalc.equivalent_potential_temperature(pres, temp, dewp)
        ept = gaussian_filter(ept, sigma=1.0)
        # 図の数、大きさを設定
        fig = plt.figure(1, figsize=(294 / 25.4, 210 / 25.4))
        # 地図の描画
        ax = self.set_ax_jp()
        # 3℃ごとに15℃まで等温線を引く
        clevs_ept = np.arange(255, 372, 3)
        cf = ax.contourf(lon, lat, ept, clevs_ept, extend='both', cmap='jet', transform=self.datacrs, alpha=0.9)
        cg = ax.contour(lon, lat, ept, clevs_ept, colors='black', linestyles='solid', transform=self.datacrs)
        plt.clabel(cg, fmt='%d')
        # 風ベクトルの表示
        wind_slice = (slice(None, None, 10), slice(None, None, 10))
        ax.barbs(lon[wind_slice], lat[wind_slice], uwnd[wind_slice].to('kt').m,
                 vwnd[wind_slice].to('kt').m, pivot='middle', color='black', alpha=0.5, transform=self.datacrs)
        # カラーバーをつける
        cbar = plt.colorbar(cf, orientation='horizontal', fraction=0.05, shrink=0.95, aspect=100, pad=0)
        cbar.set_label('E.P.TEMP (K)')
        # タイトルをつける
        plt.title('850hPa: E.P.TEMP (K), WIND ARROW (kt)', loc='left')
        plt.title(self.time_str2, loc='right')
        # 大きさの調整
        plt.subplots_adjust(bottom=0.1, top=0.9)
        # 保存
        plt.savefig(os.path.join('j850eptw', 'j850eptw_' + self.time_str1 + '.png'))
        # 閉じる
        plt.close(fig=fig)
