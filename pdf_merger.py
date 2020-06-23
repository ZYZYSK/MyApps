import tkinter
import PyPDF2
import os

root = tkinter.Tk()
root.title('PDFMerger')
root.geometry("800x700")
ver = '1.0.0'  # バージョン
# Openボタン
button = tkinter.Button(root, text="Open", width=8, height=2, font=(
    u'Meiryo', 8), bg='#add8e6', fg='#000000')
# button = tkinter.Button(root, text="Open", command=clicked, width=8, height=2, font=(u'Meiryo', 8), bg='#add8e6', fg='#000000')
button.place(x=80, y=120)

# Mergeボタン
button = tkinter.Button(root, text="Merge", width=8, height=2, font=(
    u'Meiryo', 8), bg='#4169e1', fg='#ffffff')
# button = tkinter.Button(root, text="Merge", command=merge, width=8, height=2, font=(u'Meiryo', 8), bg='#4169e1', fg='#ffffff')
button.place(x=200, y=120)

# ラベル1　パス
lbl = tkinter.Label(text='パス', font=(u'Meiryo', 8))
lbl.place(x=25, y=30)

# テキストボックス１　パス
txt1 = tkinter.Entry(width=80)
txt1.insert(tkinter.END, "パスを入力してください")
txt1.place(x=80, y=30)

# ラベル2　保存ファイル名
lbl = tkinter.Label(text='ファイル名', font=(u'Meiryo', 8))
lbl.place(x=5, y=75)

# テキストボックス２　保存ファイル名
txt2 = tkinter.Entry(width=80)
txt2.insert(tkinter.END, "merged")
txt2.place(x=80, y=75)

# テキストボックス３　ファイル
txt3 = tkinter.Text(width=80, font=(u'Meiryo', 8))
txt3.place(x=80, y=200)
txt3.insert('1.0', 'version ' + ver +
            '\n\n１．結合するPDFファイルのパスを入力\n\n２．Openボタンでファイル確認\n\n３．Mergerボタンでデスクトップに  ファイル名.pdf  を作成\n')
root.mainloop()
