import tkinter as tk
import subprocess
import os
import sys


class Application(tk.Frame):
    def __init__(self, master, programs) -> None:
        super().__init__(master)
        self.pack()
        # アプリのタイトル
        master.title('PC Manager')
        # プログラムの総数
        self.n = len(programs)
        # プログラム一覧
        self.programs = programs
        # ボタンの動作を指定
        for i in range(self.n):
            btn = tk.Button(self, text=self.programs[i][0], command=self.make_btn(i))
            btn.pack()

    def make_btn(self, i):
        return lambda: self.run(i)

    def run(self, i):
        subprocess.Popen(self.programs[i][1], shell=True)
        print('{0}: {1}が実行されました．'.format(self.programs[i][0], self.programs[i][1]))


def fix_my_pc():
    # 登録するプログラム一覧
    programs = [
        ['復元ポイントの管理', 'C:\\Windows\\System32\\SystemPropertiesProtection.exe'],
        ['システムクリーンアップ', 'C:\\WINDOWS\\system32\\cleanmgr.exe'],
        ['CrystalDiskInfo', 'C:\\Program Files\\CrystalDiskInfo\\DiskInfo64.exe'],
        ['スクリーンセーバー', 'desk.cpl,1'],
        ['アップデートと修復', '{0}\\admin.bat {0}\\updater.bat'.format(os.path.dirname(__file__))]
    ]
    win = tk.Tk()
    app = Application(master=win, programs=programs)
    app.mainloop()


if __name__ == "__main__":
    # print('プログラムを起動します．(y/n): ', end='')
    # while True:
    #     x = input()
    #     if x == 'y':
    #         break
    #     elif x == 'n':
    #         sys.exit()
    fix_my_pc()
