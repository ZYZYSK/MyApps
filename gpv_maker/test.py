import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from metpy.units import units
import numpy as np
from scipy.ndimage import gaussian_filter
import pygrib as grib
import os
os.chdir('D:\\Weather_new\\tmp')
gpv = grib.open('2020090818')
height, lat, lon = gpv.select(shortName='gh', level=500)[0].data()
temp, _, _ = gpv.select(shortName='t', level=500)[0].data()
height_500 = gaussian_filter(height, sigma=3.0)
temp_500 = (gaussian_filter(temp, sigma=3.0)
            * units.kelvin).to(units.celsius)
mapcrs = ccrs.LambertConformal(central_longitude=140,
                               central_latitude=35,
                               standard_parallels=(30, 60))
datacrs = ccrs.PlateCarree()
fig = plt.figure(1, figsize=(294 / 25.4, 210 / 25.4))
ax = plt.subplot(111, projection=mapcrs)
ax.set_extent([110, 170, 10, 60], ccrs.PlateCarree())
ax.add_feature(cfeature.COASTLINE.with_scale('50m'))
ax.add_feature(cfeature.BORDERS.with_scale('50m'))
ax.gridlines(xlocs=mticker.MultipleLocator(10),
             ylocs=mticker.MultipleLocator(10),
             linestyle='-', color='gray')
clevs_500_hght = np.arange(0, 8000, 60)
cs = ax.contour(lon, lat, height_500, clevs_500_hght,
                colors='black', transform=datacrs)
plt.clabel(cs, fmt='%d')
clevs_500_temp = np.arange(-60, 15, 3)
cs = ax.contour(lon, lat, temp_500, clevs_500_temp,
                colors='black', transform=datacrs)
plt.clabel(cs, fmt='%d')
plt.title('500-hPa Geopotential Heights (m) and Temperature(C)', loc='left')
plt.subplots_adjust(bottom=0, top=1)
plt.show()
