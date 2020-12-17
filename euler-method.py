from math import sin, pi
import matplotlib.pylab as plt

U_max = 100
frequency = 50
R1 = 5
R2 = 4
R3 = 7
R4 = 2
L1 = 0.01
L2 = 0.02
C1 = 300 * 10 ** -6
h = 0.00001


f = [lambda cur_time, value: (value[1]/C1),
     lambda cur_time, value: (U_max * sin(2 * pi * frequency * cur_time) - value[0] - value[1]*R1 + value[2]*R2)/L1,
     lambda cur_time, value: (value[1]*R1 - value[2]*R1 - value[2]*R2)/L2]


def output_voltage(value):
    print(value[2] * R2)
    return value[2] * R2


def get_next_value(current_time, value, h):
    next_value = value
    for i in range(len(value)):
        next_value[i] = value[i] + h * f[i](current_time, value)
    return next_value


def get_results(current_time, end_time, value, h):
    time_value = dict()
    while current_time < end_time:
        next_cur_time = current_time + h
        next_value = get_next_value(current_time, value, h)
        current_time = next_cur_time
        value = next_value
        time_value[current_time] = output_voltage(value)
    return time_value


def main():
    start_time = 0
    end_time = 0.2
    init_values = [0, 0, 0]

    result = get_results(start_time, end_time, init_values, h)

    results_for_each_value = []
    values = []

    for t, v in result.items():
        results_for_each_value.append(t)
        values.append(v)

    plt.plot(results_for_each_value, values)
    plt.show()


if __name__ == '__main__':
    main()
