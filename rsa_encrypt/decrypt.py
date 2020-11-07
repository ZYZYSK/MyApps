import os
import sys


class RSA_decryption:
    @classmethod
    def binary_method(cls, c, d, N):
        # 繰り返し二乗法
        if d == 0:
            return 1
        x = cls.binary_method(c, d // 2, N) % N
        m = x * x % N
        if d % 2 == 1:
            m *= (c % N)
            m %= N
        return m

    def __init__(self):
        sys.setrecursionlimit(10000)
        # 暗号ファイルのパス
        self.file_path = None
        # 暗号文用
        self.encrypted_integers = []
        # 平文用
        self.plain_integers = []
        # 共通鍵
        self.N = 0
        # 秘密鍵
        self.d = 0

    def get_encrypted_integer(self):
        # 暗号文を取得
        while True:
            print("暗号ファイルのパス(例: C:\\Documents\\file.txt): ", end='')
            self.file_path = input()
            try:
                with open(self.file_path, mode='r', encoding="utf-8") as f:
                    string = f.read().split()
                    self.encrypted_integers = [int(i) for i in string]
            except Exception as e:
                print('ファイルを開けませんでした.')
            else:
                break

    def get_keys(self):
        # 鍵を取得
        print("鍵1, 鍵2をそれぞれ入力してください: ")
        print("鍵1: ", end='')
        self.N = int(input())
        print("鍵2: ", end='')
        self.d = int(input())

    def decryption(self):
        # 復号化
        for c in self.encrypted_integers:
            self.plain_integers.append(self.binary_method(c, self.d, self.N))

    def output_plain_text(self):
        # 平文を出力
        with open(self.file_path + '_plain.txt', mode='w', encoding="utf-8")as f:
            f.writelines([chr(i) for i in self.plain_integers])
            print(self.file_path + '_plain.txt に復号しました')


def decrypt():
    a = RSA_decryption()
    # 暗号文の取得
    a.get_encrypted_integer()
    # 鍵の取得
    a.get_keys()
    # 復号化
    a.decryption()
    # 平文を出力
    a.output_plain_text()


if __name__ == "__main__":
    decrypt()
    print('\'q\'で終了します')
    while True:
        s = input()
        if s == 'q':
            sys.exit()
