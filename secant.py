import math


def f(x):
    return math.cos(x-1) - 3*x + 2


def fd(x):
    return -3 + math.sin(1-x)


def check(x):
    print(f(x))


def compute_secant():
    x = -2
    x0 = x
    x = fd(x0)
    eps = 0.01
    while True:
        x00 = x0
        x0 = x
        fx00 = f(x00)
        fx = f(x)
        x = x - fx/((fx00 - fx)/(x00 - x))
        print(abs((x - x0) / x))
        if abs((x - x0) / x) < eps:
            break
    check(x)


if __name__ == '__main__':
    compute_secant()
