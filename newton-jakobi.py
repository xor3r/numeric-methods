def f1(x1, x2):
    return x2**2 - x1**2 - 0.1 - x1


def f2(x1, x2):
    return 0.1 - 2*x1*x2 - x2


def newton_jakobi():
    eps = 0.001
    argument_vector = [0.5, 0.5]
    prev_vector = [0, 0]
    identity_matrix = initialize_matrix()
    f = [0, 0]
    while True:
        f[0] = f1(argument_vector[0], argument_vector[1])
        f[1] = f2(argument_vector[0], argument_vector[1])
        jacobian = build_jacobian(argument_vector, f)
        reversed_jacobian = reverse_matrix(jacobian, identity_matrix)
        for i in range(len(f)):
            x_old = argument_vector[i]
            prev_vector[i] = x_old
            increment = 0.0
            for j in range(2):
                increment += reversed_jacobian[i][j] * f[i]
            argument_vector[i] = prev_vector[i] - increment
        if abs((argument_vector[0] - prev_vector[0])/argument_vector[0]) < eps:
            break
        elif abs((argument_vector[1] - prev_vector[1])/argument_vector[1]) < eps:
            break

    print(argument_vector)
    print(f1(argument_vector[0], argument_vector[1]))
    print(f2(argument_vector[0], argument_vector[1]))


def build_jacobian(argument_vector, function_vector):
    h = 1
    args = [0, 0]
    f = [0, 0]
    jacobian = [[0, 0], [0, 0]]
    for i in range(2):
        for j in range(2):
            for k in range(2):
                args[k] = argument_vector[k]
            args[j] = argument_vector[j] + h
            f[0] = f1(args[0], args[1])
            f[1] = f2(args[0], args[1])
            jacobian[i][j] = (f[i] - function_vector[i])/h
    return jacobian


def initialize_matrix():
    matrix = [[0 for _ in range(4)] for _ in range(4)]
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if i == j:
                matrix[i][j] = 1
            else:
                matrix[i][j] = 0
    return matrix


def reverse_matrix(matrix, identity_matrix):
    size = len(matrix)
    reversed_matrix = [[0 for _ in range(size)] for _ in range(size)]
    for i in range(size):
        solution = roots(i, matrix, identity_matrix)
        for j in range(len(solution)):
            reversed_matrix[j][i] = solution[j]
    return reversed_matrix


def roots(counter, matrix, identity_matrix):
    size = len(matrix)
    coefficients = [[0 for _ in range(size)] for _ in range(size)]
    free_members = [0 for _ in range(size)]
    argument_positions = [0 for _ in range(size)]
    result_coefficients = [[0 for _ in range(size)] for _ in range(size)]
    result_free_members = [0 for _ in range(size)]
    free_members, coefficients, argument_positions = initialize_system(
        free_members, identity_matrix, counter, argument_positions, coefficients, matrix)
    result_free_members, free_members, coefficients, result_coefficients = direct_way(
        result_free_members, free_members, coefficients, result_coefficients, argument_positions, size)
    result = reverse_way(result_free_members, result_coefficients)
    result, argument_positions = order_vector(result, argument_positions)
    return result


def order_vector(result, argument_positions):
    for i in range(len(result)):
        if argument_positions != i:
            arg = argument_positions[i]
            value = result[i]
            result[i] = result[arg]
            result[arg] = value
            argument_positions[i] = argument_positions[arg]
            argument_positions[arg] = arg
    return result, argument_positions


def direct_way(result_free_members, free_members, coefficients, result_coefficients, argument_positions, size):
    for i in range(size):
        coefficients, free_members, argument_positions, result_coefficients = optimize_matrix(
            i, coefficients, free_members, argument_positions, result_coefficients, size)
        result_free_members[i] = free_members[i] / coefficients[i][i]
        for j in range(i + 1, size):
            free_members[j] = free_members[j] - coefficients[j][i] * result_free_members[i]
            for k in range(i + 1, size):
                result_coefficients[i][k] = coefficients[i][k] / coefficients[i][i]
                coefficients[j][k] = coefficients[j][k] - coefficients[j][i] * result_coefficients[i][k]
    return result_free_members, free_members, coefficients, result_coefficients


def reverse_way(result_free_members, result_coefficients):
    size = len(result_free_members)
    solution = [0 for _ in range(size)]
    for i in range(size -1, -1, -1):
        sum = 0.0
        for j in range(i + 1, size):
            sum += result_coefficients[i][j] * solution[j]
        solution[i] = result_free_members[i] - sum
    return solution


def initialize_system(free_members, identity_matrix, counter, argument_positions, coefficients, matrix):
    size = len(matrix)
    for i in range(size):
        free_members[i] = identity_matrix[i][counter]
        argument_positions[i] = i
        for j in range(size):
            coefficients[i][j] = matrix[i][j]
    return free_members, coefficients, argument_positions


def optimize_matrix(r, coefficients, free_members, argument_positions, result_coefficients, size):
    max_coefficient = coefficients[r][r]
    max_row = r
    max_col = r
    for i in range(size):
        for j in range(size):
            if max_coefficient < abs(coefficients[i][j]):
                max_coefficient = abs(coefficients[i][j])
                max_row = i
                max_col = j
    free_members = swap_array_values(free_members, r, max_row)
    for l in range(size):
        coefficients = swap_matrix_values_row(coefficients, r, max_row, l)
    argument_positions = swap_argument_positions(argument_positions, r, max_col)
    for m in range(size):
        if m < r:
            result_coefficients = swap_matrix_values_columns(result_coefficients, m, r, max_col)
        else:
            coefficients = swap_matrix_values_columns(coefficients, m, r, max_col)
    return coefficients, free_members, argument_positions, result_coefficients


def swap_matrix_values_columns(matrix, r, fc, sc):
    temp = matrix[r][fc]
    matrix[r][fc] = matrix[r][sc]
    matrix[r][sc] = temp
    return matrix


def swap_argument_positions(argument_positions, r, max_col):
    temp = argument_positions[r]
    argument_positions[r] = argument_positions[max_col]
    argument_positions[max_col] = temp
    return argument_positions


def swap_array_values(free_members, fc, sc):
    temp = free_members[fc]
    free_members[fc] = free_members[sc]
    free_members[sc] = temp
    return free_members


def swap_matrix_values_row(matrix, fc, sc, col):
    temp = matrix[fc][col]
    matrix[fc][col] = matrix[sc][col]
    matrix[sc][col] = temp
    return matrix


if __name__ == '__main__':
    newton_jakobi()
