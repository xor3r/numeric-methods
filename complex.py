from math import ceil
import matplotlib.pylab as plt
import numpy as np

C1 = 1 * 10 ** -3
C2 = 2 * 10 ** -3
L_min = 0.2
L_max = 2
i_min = 1
i_max = 2
R1 = 23
R2 = 33
R3 = 40
half_period = 0.004
period = 2 * half_period

differential_equations = \
    [lambda time_point, value: ((input_voltage(time_point) - value[2])/C1),
     lambda time_point, value: ((-value[1] * (R2 + R3))/inductance(value[1])),
     lambda time_point, value: ((input_voltage(time_point) - value[2]) / C2)]


def draw_graph(x_arguments, y_values, title="", x_label="", y_label=""):
    graph = plt.figure().gca()
    graph.plot(x_arguments, y_values)
    graph.set_title(title)
    graph.set_xlabel(x_label)
    graph.set_ylabel(y_label)
    plt.show()


def input_voltage(time_point):
    number_of_half_periods = ceil(time_point / half_period)
    if number_of_half_periods % 2:
        return 10 / half_period * (time_point - (number_of_half_periods - 1) * half_period)
    return 0


def output_voltage(value):
    return value[2]


def inductance(current_value):
    if abs(current_value) <= i_min:
        return L_max
    if abs(current_value) >= i_max:
        return L_min
    A = np.array(
        [
            [1, i_min, i_min ** 2, i_min ** 3, L_max],
            [1, i_max, i_max ** 2, i_max ** 3, L_min],
            [0, 1, 2 * i_min, 3 * i_min ** 2, 0],
            [0, 1, 2 * i_max, 3 * i_max ** 2, 0]
        ])
    a = solve_lu(A)
    return a[0] + a[1]*abs(current_value) + a[2]*current_value**2 + a[3]*abs(current_value**3)


def solve_lu(A):
    n = len(A)
    b = [0 for i in range(n)]
    for i in range(0, n):
        b[i] = A[i][n]
    L = [[0 for i in range(n)] for i in range(n)]
    for i in range(0, n):
        L[i][i] = 1
    U = [[0 for i in range(0, n)] for i in range(n)]
    for i in range(0, n):
        for j in range(0, n):
            U[i][j] = A[i][j]
    n = len(U)
    for i in range(0, n):
        maxElem = abs(U[i][i])
        maxRow = i
        for k in range(i + 1, n):
            if abs(U[k][i]) > maxElem:
                maxElem = abs(U[k][i])
                maxRow = k
        for k in range(i, n):
            tmp = U[maxRow][k]
            U[maxRow][k] = U[i][k]
            U[i][k] = tmp
        for k in range(i + 1, n):
            c = -U[k][i] / float(U[i][i])
            L[k][i] = c
            for j in range(i, n):
                U[k][j] += c * U[i][j]
        for k in range(i + 1, n):
            U[k][i] = 0
    n = len(L)
    y = [0 for i in range(n)]
    for i in range(0, n, 1):
        y[i] = b[i] / float(L[i][i])
        for k in range(0, i, 1):
            y[i] -= y[k] * L[i][k]
    n = len(U)
    x = [0 for i in range(n)]
    for i in range(n - 1, -1, -1):
        x[i] = y[i] / float(U[i][i])
        for k in range(i - 1, -1, -1):
            U[i] -= x[i] * U[i][k]
    return x


def get_next_value(time_point, value, step):
    """Runge-Kutta"""
    next_value = value

    for i in range(len(value)):
        this_value = value[i]
        coefficient1 = step * differential_equations[i](time_point, value)
        value[i] = this_value + 1/3 * coefficient1
        coefficient2 = step * differential_equations[i](time_point + 1/3 * step, value)
        value[i] = this_value - 1/3 * coefficient1 + coefficient2
        coefficient3 = step * differential_equations[i](time_point + 2/3 * step, value)
        value[i] = this_value + coefficient1 - coefficient2 + coefficient3
        coefficient4 = step * differential_equations[i](time_point + step, value)
        value[i] = this_value

        next_value[i] = value[i] + (coefficient1 + 3 * (coefficient2 + coefficient3) + coefficient4) / 8

    return next_value


def get_results(time_point, time_interval, value, step):
    time_value_pairs = dict()
    time_value_pairs[time_point] = [value[0], value[1], value[2], input_voltage(time_point), output_voltage(value)]
    while time_point < time_interval:
        value = get_next_value(time_point, value, step)
        time_point += step
        time_value_pairs[time_point] = [value[0], value[1], value[2], input_voltage(time_point), output_voltage(value)]
    return time_value_pairs


def main():
    time_point = 0
    value = [1, 1, 1]
    time_interval = 5 * period
    step = period / 100
    time_value_pairs = get_results(time_point, time_interval, value, step)

    time_points = []
    values_u_c1 = []
    values_u_c2 = []
    values_i_l2 = []
    values_u1 = []
    values_u2 = []
    values_of_inductance = []

    i_interval = []
    i = 0
    while i <= i_max + 1:
        i_interval.append(i)
        values_of_inductance.append(inductance(i))
        i += step

    for t, v in time_value_pairs.items():
        time_points.append(t)
        values_u_c1.append(v[0])
        values_u_c2.append(v[2])
        values_i_l2.append(v[1])
        values_u1.append(v[3])
        values_u2.append(v[4])

    draw_graph(i_interval, values_of_inductance, "L2", "i, amp", "L, henry")
    draw_graph(time_points, values_u1, "U1", "t, sec", "u, volt")
    draw_graph(time_points, values_u_c1, "U_C1", "t, sec", "u, volt")
    draw_graph(time_points, values_u_c2, "U_C2", "t, sec", "u, volt")
    draw_graph(time_points, values_i_l2, "i_L2", "t, sec", "i, amp")
    draw_graph(time_points, values_u2, "U2", "t, sec", "u, volt")


if __name__ == '__main__':
    main()
