import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from matplotlib.colors import Normalize
from matplotlib.colors import ListedColormap
from metpy.units import units
import metpy.calc as mpcalc
import numpy as np
from scipy.ndimage import gaussian_filter
import pygrib as grib
import os
os.chdir('C:\\Users\\huang\\Downloads')
gpv = grib.open('2020091500')
# 500hPa高度、緯度、経度の取得
height, lat, lon = gpv.select(shortName='gh', level=500)[0].data()
# 500hPa風の取得
uwnd_500, _, _ = gpv.select(shortName='u', level=500)[0].data()*units('m/s')
vwnd_500, _, _ = gpv.select(shortName='v', level=500)[0].data()*units('m/s')

# 渦度の計算
dx, dy = mpcalc.lat_lon_grid_deltas(lon, lat)
avor = mpcalc.vorticity(uwnd_500, vwnd_500, dx, dy, dim_order='yx')
# 高度線を滑らかにする
height_500 = gaussian_filter(height, sigma=3.0)
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
# カラーマップを作成する
N = 360
M = 120
red = np.ones((N, 4))
blue = np.ones((M, 4))
red[:, 0] = np.linspace(1, 1, N)
red[:, 1] = np.linspace(1, 0, N)
red[:, 2] = np.linspace(1, 0, N)
blue[:, 0] = np.linspace(0, 1, M)
blue[:, 1] = np.linspace(0, 1, M)
blue[:, 2] = np.linspace(1, 1, M)
cmap = np.vstack((blue, red))
bwr_new = ListedColormap(cmap)
# 等渦度線を引く
clevs_500_vort = np.arange(-120, 360, 20)
cf = ax.contourf(lon, lat, avor*10**6, clevs_500_vort, extend='both',
                 cmap=bwr_new, transform=datacrs, alpha=0.9)
# カラーバーをつける
cbar = plt.colorbar(cf, orientation='horizontal',
                    fraction=0.05, shrink=7/8, aspect=100, pad=0)
cbar.set_label('<Vorticity ($10^{-6}/s$)>')
# タイトルをつける
plt.title(
    '500-hPa Geopotential Heights (m) and Vorticity ($10^{-6}/s$)', loc='left')
plt.subplots_adjust(bottom=0.1, top=0.9)
plt.savefig(os.path.join('500hvj', '500hvj_'+'2020091500'+'.png'))
