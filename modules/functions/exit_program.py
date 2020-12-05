import os
import sys
from tkinter import messagebox


def exit_program(e, info=None):  # プログラムの終了
    # info=sys.exec_info()
    if not info is None:
        exc_type, exc_obj, exc_tb = info
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print("{0} {1} {2}行目".format(exc_type, fname, exc_tb.tb_lineno))
    print("{0}\n\'q\'で終了します".format(e))
    while True:
        s = input()
        if s == 'q':
            sys.exit()


def exit_program_tk(error_title, error_content, master=None):  # プログラムの終了(tkinter)
    messagebox.showerror(error_title, error_content)
    if master:
        master.destroy()
    sys.exit()


def handler_sigint(signal, frame):  # SIGINTシグナルハンドラ
    exit_program("SIGINTシグナルが送信されました．")


def handler_sigint_tk(signal, frame):  # SIGINTシグナルハンドラ(tkinter)
    exit_program_tk("エラー", "SIGINTシグナルが送信されました")
