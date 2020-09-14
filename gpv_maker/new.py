import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from matplotlib.colors import Normalize
from metpy.units import units
import numpy as np
from scipy.ndimage import gaussian_filter
import pygrib as grib
import os
os.chdir('D:\\Weather_new\\tmp')
gpv = grib.open('2020090812')
# 500hPa高度、緯度、経度の取得
height, lat, lon = gpv.select(shortName='gh', level=500)[0].data()
# 500hPa気温の取得
vort = gpv.select(shortName='vort', level=500)[0].data()
# 高度線を滑らかにする
height_500 = gaussian_filter(height, sigma=3.0)
# 温度線を滑らかにする
vort_500 = (gaussian_filter(vort, sigma=3.0)
            * units.kelvin).to(units.celsius)
# mapcrs=ランベルト正角円錐図法(中心緯経線と標準緯線の設定)
mapcrs = ccrs.LambertConformal(central_longitude=140,
                               central_latitude=35,
                               standard_parallels=(30, 60))
# datacrs=正距円筒図法
datacrs = ccrs.PlateCarree()
# 図の数、大きさを設定
fig = plt.figure(1, figsize=(294 / 25.4, 210 / 25.4))
# 描画キャンパスを1行1列に分割し、1枚目をaxとする。
ax = plt.subplot(111, projection=mapcrs)
# 緯度、経度の範囲を設定
ax.set_extent([110, 170, 10, 60], datacrs)
# 海岸線の細かさ(10m,50m,110m)
ax.add_feature(cfeature.COASTLINE.with_scale('50m'))
# 国境線の細かさ(10m,50m,110m)
ax.add_feature(cfeature.BORDERS.with_scale('50m'))
# 陸を塗りつぶす
ax.add_feature(cfeature.LAND, color='grey', alpha=0.6)
# 格子線の大きさ、色、線種、間隔の設定(ここでは緯線と経線をひく)
ax.gridlines(xlocs=mticker.MultipleLocator(10),
             ylocs=mticker.MultipleLocator(10),
             linestyle=':', color='grey')
# 60mごとに8000mまで等高度線を引く
clevs_500_hght = np.arange(0, 8000, 60)
cs = ax.contour(lon, lat, height_500, clevs_500_hght,
                colors='black', transform=datacrs)
plt.clabel(cs, fmt='%d')
# 3℃ごとに15℃まで等温線を引く
clevs_500_vort = np.arange(0, 400, 40)
cf = ax.contourf(lon, lat, vort_500, clevs_500_vort,
                 cmap='Purples', transform=datacrs, alpha=0.9)
# カラーバーをつける
cbar = plt.colorbar(cf, orientation='horizontal',
                    fraction=0.05, shrink=7/8, aspect=100, pad=0)
cbar.set_label('<Vorticity(10**-6/SEC)>')
# タイトルをつける
plt.title(
    '500-hPa Geopotential Heights (m) and Vorticity(10**-6/SEC)', loc='left')
plt.subplots_adjust(bottom=0.1, top=0.9)
plt.savefig('test.png')
