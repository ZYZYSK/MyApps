import os
import re
import serial
from serial.tools import list_ports
import time
import datetime


def main():
    SERIAL_SPEED = 9600
    BRIGHTNESS_BORDER = 20
    old_isdark = -1
    new_isdark = -1
    old_time = datetime.datetime.now()-datetime.timedelta(minutes=5)
    new_time = datetime.datetime.now()
    while True:
        DEV_NAME = get_devname()
        if DEV_NAME == 0:
            print('Arduinoが接続されていません')
        else:
            try:
                data = serial.Serial(DEV_NAME, SERIAL_SPEED, timeout=None)
            except Exception as e:
                print(e)
            else:
                line = data.readline()
                data.close()
                brightness = get_number(line)
                print(brightness)
                new_time = datetime.datetime.now()
                if brightness == -1:
                    pass
                elif new_time-datetime.timedelta(minutes=5) >= old_time:
                    if brightness <= BRIGHTNESS_BORDER:
                        new_isdark = 1
                        if new_isdark != old_isdark:
                            os.system('powershell -Command'+' ' +
                                      'powershell -ExecutionPolicy RemoteSigned .\\darkmode.ps1')
                        old_isdark = 1
                    else:
                        new_isdark = 0
                        if new_isdark != old_isdark:
                            os.system('powershell -Command'+' ' +
                                      'powershell -ExecutionPolicy RemoteSigned .\\lightmode.ps1')
                        old_isdark = 0
                    old_time = datetime.datetime.now()
        time.sleep(5)


def get_devname():
    ports = list_ports.comports()
    device = [info for info in ports if 'Arduino' in info.description]
    if len(device):
        return device[0].device
    else:
        return 0


def get_number(line):
    try:
        brightness = int(re.search('\d+', line.decode()).group())
    except Exception as e:
        print(e)
        brightness = -1
    finally:
        return brightness


if __name__ == "__main__":
    main()
