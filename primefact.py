def main():
    print('数字を入力してください：', end='')
    a = int(input())
    l = [i for i in range(0, a + 1)]
    p = 2
    while p * p <= a:
        if l[p] == p:
            for i in range(2 * p, a + 1, p):
                l[i] = p
        p += 1
    while a > 1:
        print(l[a])
        a //= l[a]


if __name__ == "__main__":
    main()
