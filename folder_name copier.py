# パス下のフォルダ名だけをコピーするプログラム(サブフォルダは含めない)
import os
import glob


def path_copy():
    print('指定したパス下のフォルダ名だけをコピーするプログラムです。')
    while True:
        print('サブフォルダは含めますか？(y/n)')
        include_sub = input('>>')
        if include_sub == 'y' or include_sub == 'n':
            break
    m_path_in, m_path_out = input_path()
    if (include_sub == 'y'):
        sub_y(m_path_in, m_path_out)
    else:
        sub_n(m_path_in, m_path_out)


def input_path():
    while True:
        print('コピー元のパスを入力してください：')
        m_path_in = input('>>')
        if os.path.isdir(m_path_in) == True:
            break
    print('コピー先のパスを入力してください：(current:カレントディレクトリ)')
    m_path_out = input('>>')
    return m_path_in, m_path_out


def sub_y(path_in, path_out):
    if path_out != 'current':
        os.makedirs(path_out, exist_ok=True)
    elif path_out == 'current':
        path_out = os.getcwd()
    for files_dir in glob.glob(os.path.join(path_in, '**/'), recursive=True):
        files_dir = (files_dir.replace(path_in, path_out)).rstrip('\\')
        print(files_dir)
        os.makedirs(files_dir, exist_ok=True)


def sub_n(path_in, path_out):
    files = os.listdir(path_in)
    files_dir = [f for f in files if os.path.isdir(os.path.join(path_in, f))]
    if path_out != 'current':
        os.makedirs(path_out, exist_ok=True)
        os.chdir(path_out)
    for i in files_dir:
        print(i)
        os.makedirs(i, exist_ok=True)


if __name__ == '__main__':
    path_copy()
