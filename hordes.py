import math


def f(x):
    return math.cos(x-1) - 3*x + 2


def fd(x):
    return -3 + math.sin(1-x)


def check(x):
    print(f(x))


def compute_hordes():
    a = -2
    b = 3
    eps = 0.01
    while True:
        fa = f(a)
        fb = f(b)
        x1 = a - fa*(b-a)/(fb-fa)
        fx1 = f(x1)
        if fx1*fa > 0:
            a = x1
            x2 = b
        else:
            b = x1
            x2 = a
        fx2 = f(x2)
        dfx2 = fd(x2)
        x2 = x2 - fx2/dfx2
        if a == x1:
            b = x2
        else:
            a = x2
        if abs((x1 - x2) / x1) < eps:
            break
    x = (x1 + x2)/2
    check(x)


if __name__ == '__main__':
    compute_hordes()
