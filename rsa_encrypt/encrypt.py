from math import e
import sys
import random
import math
import os


class RSA_encryption:
    MIN = 1 << 32
    MAX = 1 << 33

    @classmethod
    def binary_method(cls, m, e, N):
        # 繰り返し二乗法
        if e == 0:
            return 1
        x = cls.binary_method(m, e // 2, N) % N
        c = x * x % N
        if e % 2 == 1:
            c *= (m % N)
            c %= N
        return c

    @classmethod
    def create_prime(cls, n):
        # 素数生成
        isprime = False
        while True:
            isprime = True
            for i in range(3, int(math.sqrt(n)) + 1, 2):
                if n % i == 0:
                    isprime = False
                    break
            if isprime:
                break
            n -= 2
        return n

    @classmethod
    def create_open_key(cls, L):
        # 公開鍵の作成
        # Lと互いに素なeを見つける
        while True:
            e = random.randrange(L / 2 + 1, L)
            while e < L:
                if math.gcd(L, e) == 1:
                    return e
                e += 1

    @classmethod
    def create_private_key(cls, L, e):
        # 秘密鍵の生成
        # Lx+ed=1=gcd(L,e)となるようなdを求める
        r0 = L; r1 = e; r2 = r0 % r1
        x0 = 1; x1 = 0; x2 = 0
        y0 = 0; y1 = 1; y2 = 0
        q = 0
        while r2:
            q = r0 // r1
            x2 = x0 - x1 * q
            y2 = y0 - y1 * q
            r0 = r1; r1 = r2
            x0 = x1; x1 = x2
            y0 = y1; y1 = y2
            r2 = r0 % r1
        if y1 < 0:
            y1 += L * math.ceil(abs(y1) / L)
        return y1

    def __init__(self) -> None:
        sys.setrecursionlimit(10000)
        # 素数生成
        self.prime_p = self.create_prime(random.randrange(self.MIN + 1, self.MAX - 1, 2))
        self.prime_q = self.create_prime(random.randrange(self.MIN + 1, self.MAX - 1, 2))
        # 共通鍵N
        self.N = self.prime_p * self.prime_q
        # L
        self.L = (self.prime_p - 1) * (self.prime_q - 1)
        # 公開鍵e
        self.e = self.create_open_key(self.L)
        # 秘密鍵d
        self.d = self.create_private_key(self.L, self.e)
        # 平文用
        self.plain_integers = []
        # 暗号用
        self.encrypted_integers = []
        # 平文ファイルのパス
        self.file_path = None

    def get_plain_integer(self):
        # 平文を取得
        while True:
            print("平文ファイルのパス(例: C:\\Documents\\file.txt): ", end='')
            self.file_path = input()
            try:
                with open(self.file_path, mode='r', encoding="utf-8") as f:
                    self.plain_integers = [ord(i) for i in f.read()]
            except Exception as e:
                print('ファイルを開けませんでした.')
            else:
                break

    def encryption(self):
        # 暗号化
        for m in self.plain_integers:
            self.encrypted_integers.append(self.binary_method(m, self.e, self.N))

    def output_encrypted_text(self):
        # 暗号文を出力
        with open(self.file_path + '_encrypted.txt', mode='w')as f:
            for i in self.encrypted_integers:
                f.write(str(i) + ' ')
            print(self.file_path + '_encrypted.txt に暗号文を出力しました')

    def get_private_key(self):
        # 秘密鍵を取得
        return self.N, self.d


def encrypt():
    a = RSA_encryption()
    # 平文を取得
    a.get_plain_integer()
    # 暗号化
    a.encryption()
    # 暗号文を出力
    a.output_encrypted_text()
    # 鍵の表示(N,d)
    print('(鍵1,鍵2) = ', a.get_private_key())
    # 終了処理
    print("鍵を保管してください！鍵をなくすと復号できなくなります！")


if __name__ == "__main__":
    encrypt()
    print('\'q\'で終了します')
    while True:
        s = input()
        if s == 'q':
            sys.exit()
