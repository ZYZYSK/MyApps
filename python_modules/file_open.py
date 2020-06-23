import os


def open_file(file_name):
    try:
        f = open(file_name, mode='r')
        folder_path = f.readline()
        os.makedirs(folder_path, exist_ok=True)
        os.chdir(folder_path)
    except FileNotFoundError:
        f = open(file_name, mode='x')
    finally:
        f.close()
