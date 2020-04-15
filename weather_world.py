import os
import datetime
import cv2
import numpy as np
import glob
from python_modules import weather_world_mover
from python_modules import file_open
from python_modules import file_download


def get_image_A():
    file_open.open_file('weather_world_setting.txt')
    a = datetime.datetime.now()
    if (a.hour >= 12):
        a = datetime.datetime.now() - datetime.timedelta(hours=a.hour) + \
            datetime.timedelta(hours=9)
    else:
        a = datetime.datetime.now() - datetime.timedelta(days=1) - \
            datetime.timedelta(hours=a.hour) + datetime.timedelta(hours=21)
    base = a.strftime("%Y%m%d%H")
    get_image_B('http://wxmaps.org/pix/avnmr', base, 'north-america_')
    get_image_B('http://wxmaps.org/pix/sa', base, 'south-america_')
    get_image_B('http://wxmaps.org/pix/euro', base, 'europe_')
    get_image_B('http://wxmaps.org/pix/ea', base, 'east-asia_')
    get_image_B('http://wxmaps.org/pix/af', base, 'africa_')
    get_image_B('http://wxmaps.org/pix/casia', base, 'central-asia_')
    get_image_B('http://wxmaps.org/pix/aus',
                base, 'australia&new-zealand_')
    get_image_C()


def get_image_B(url_base, base, image_type):
    for i in range(1, 8):
        if not os.path.isfile(image_type+str(i)+'_'+base+'00.png') == True:
            url = url_base + str(i) + '.00hr.png'
            image_name = image_type+str(i)+'_'+base+'00.png'
            while True:
                if file_download.download_file(url, image_name) == True:
                    break


def get_image_C():
    a = datetime.datetime.today()
    a = datetime.datetime.today() - datetime.timedelta(days=2)
    base = a.strftime("%Y%m%d")
    if not os.path.isfile('ice_'+base+'.png') == True:
        url = 'https://www.natice.noaa.gov/pub/ims/ims_gif/DATA/prvsnow.gif'
        image_name = 'ice_'+base+'.png'
        while True:
            if file_download.download_file(url, image_name) == True:
                break


def edit_image_A():
    for x in glob.glob('*.png'):
        if not x[:3] == 'ice':
            edit_image_B(x, x.split('_')[0])


def edit_image_B(image_name, image_type):
    img1 = cv2.imread(image_name)
    base = cv2.imread('base/'+image_type+'.png')
    height, width, color = img1.shape
    dst = np.zeros((height, width, 3), dtype="uint8")
    for y in range(0, height):
        for x in range(0, width):
            if(base[y][x] > 240).all():
                dst[y][x] = img1[y][x]
            else:
                dst[y][x] = 0
    os.remove(image_name)
    cv2.imwrite(image_name, dst)


if __name__ == "__main__":
    get_image_A()
    edit_image_A()
    weather_world_mover.move_image_A()
