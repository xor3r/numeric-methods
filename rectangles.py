import math


def f(x):
    return 1/(x*(1+2*x)**2)


def F(x):
    return 1/(1+2*x) - math.log((1+2*x)/x)


def check(a, b):
    print(abs(F(b) - F(a)))


def compute_right_rectangles(interactive=False):
    integral = 0
    a = int(input("Enter lower bound: ")) if interactive else 1
    b = int(input("Enter upper bound: ")) if interactive else 2
    n = int(input("Enter number of divisions: ")) if interactive else 100
    h = (b - a)/n
    x = a
    for i in range(1, n):
        integral += f(x)
        x += h
    integral *= h
    print(integral)
    check(a, b)


if __name__ == '__main__':
    compute_right_rectangles()
