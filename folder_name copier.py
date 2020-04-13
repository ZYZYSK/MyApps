# パス下のフォルダ名だけをコピーするプログラム(サブフォルダは含めない)
# ver.2ではサブフォルダを含めてコピーできる機能を追加
import os


def path_copy():
    print('指定したパス下のフォルダ名だけをコピーするプログラムです。')
    while True:
        print('コピー元のパスを入力してください：')
        m_path = input('>>')
        try:
            files = os.listdir(m_path)
        except:
            continue
        break
    files_dir = [f for f in files if os.path.isdir(os.path.join(m_path, f))]
    while True:
        print('コピー先のパスを入力してください：(current:カレントディレクトリ)')
        m_path = input('>>')
        if m_path == 'current':
            for i in files_dir:
                os.makedirs(i, exist_ok=True)
            break
        else:
            try:
                os.chdir(m_path)
            except:
                os.makedirs(m_path)
                os.chdir(m_path)

            for i in files_dir:
                os.makedirs(i, exist_ok=True)
            break


path_copy()
