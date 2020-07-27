

class A:
    def __init__(self):
        self.name = "test"

    def print1(self):
        print3()

    def print2(self):
        print(self.name)


def print3():
    print("test")


a = A()
a.print1()
print(int(7)//int(5)*int(5))
