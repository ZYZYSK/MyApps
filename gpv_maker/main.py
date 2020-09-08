from func import *


def main():
    settings = get_settings('settings.txt')
    location = settings[0]
    move_location(location, time_start)


if __name__ == '__main__':
    main()
