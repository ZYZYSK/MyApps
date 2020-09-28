import tkinter as tk
from viewer import *


def main():
    # デフォルト画面を表示
    win = tk.Tk()
    app = Viewer_Base(master=win)
    app.mainloop()


if __name__ == "__main__":
    main()
