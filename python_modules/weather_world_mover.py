import os
import glob
import shutil


def move_image_A():
    for x in glob.glob('*.png',):
        if x.split('_')[0] == 'ice':
            move_image_C(x, x.split('_')[1])
        else:
            move_image_B(x, x.split('_')[0], x.split(
                '_')[1], x.split('_')[2])


def move_image_B(image, image_region, image_type, image_time):
    m_time = image_time[:4] + '_' + image_time[5:6]
    m_path = os.path.join(image_type, image_region, m_time)
    os.makedirs(m_path, exist_ok=True)
    try:
        shutil.move(image, m_path + '/')
    except shutil.Error:
        os.remove(image)


def move_image_C(image, image_time):
    m_time = image_time[:4]
    m_path = os.path.join('ice', m_time)
    os.makedirs(m_path, exist_ok=True)
    try:
        shutil.move(image, m_path + '/')
    except shutil.Error:
        os.remove(image)
