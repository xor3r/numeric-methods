import math


def f(x):
    return math.cos(x-1) - 3*x + 2


def check(x):
    print(f(x))


def compute_steffensen(interactive=False):
    eps = float(input("Enter deviation: ")) if interactive else 0.01
    x = float(input("Enter X: ")) if interactive else -2
    while True:
        x0 = x
        fx = f(x)
        z = x + fx
        fz = f(z)
        x = x - (fx/(fz-fx))*fx
        if abs((x - x0) / x) < eps:
            break
    print(x)
    check(x)


if __name__ == '__main__':
    compute_steffensen()
