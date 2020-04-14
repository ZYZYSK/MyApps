import os
import requests
import datetime
import cv2
import numpy as np
import glob
import weather_world_mover


def get_image_A():
    try:
        f = open('weather_world_setting.txt', mode='r')
        folderpath = f.readline()
        os.chdir(folderpath)
    except FileNotFoundError:
        f = open('weather_world_setting.txt', mode='x')
    finally:
        f.close()
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
            while True:
                try:
                    req = requests.get(url)
                except (ConnectionError, ConnectionAbortedError, ConnectionRefusedError, ConnectionResetError):
                    pass
                else:
                    break
            with open(image_type+str(i)+'_'+base+'00.png', "wb") as w:
                w.write(req.content)
                w.close()


def get_image_C():
    a = datetime.datetime.today()
    a = datetime.datetime.today() - datetime.timedelta(days=2)
    base = a.strftime("%Y%m%d")
    if not os.path.isfile('ice_'+base+'.png') == True:
        url = 'https://www.natice.noaa.gov/pub/ims/ims_gif/DATA/prvsnow.gif'
        while True:
            try:
                req = requests.get(url)
            except (ConnectionError, ConnectionAbortedError, ConnectionRefusedError, ConnectionResetError):
                pass
            else:
                break
        with open('ice_'+base+'.png', "wb") as w:
            w.write(req.content)
            w.close()


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


get_image_A()
edit_image_A()
weather_world_mover.move_image_A()
