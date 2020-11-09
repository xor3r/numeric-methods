import math


def f(x):
    return math.cos(x-1) - 3*x + 2


def check(x):
    print(f(x))


def compute_steffensen():
    eps = 0.01
    x = -2
    while True:
        x0 = x
        fx = f(x)
        z = x + fx
        fz = f(z)
        x = x - (fx/(fz-fx))*fx
        if abs((x - x0) / x) < eps:
            break
    check(x)


if __name__ == '__main__':
    compute_steffensen()
