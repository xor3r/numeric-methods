import copy


def gauss_eq(a, b):
    inx = [1,2,3,4]
    v = copy.deepcopy(a)
    p = copy.deepcopy(b)
    y = copy.deepcopy(p)
    c = copy.deepcopy(a)
    n = len(a)
    for i in range(1,n):
        inx[i] = i
    for i in range(1,n):
        for j in range(1, n):
            v[i][j] = a[i][j]
            p[i] = b[i]
    for k in range(1,n):
        max = abs(v[k][k])
        h = k
        w = k
        for l in range(k, n):
            for f in range(k, n):
                if max < abs(v[l][f]):
                    max = abs(v[l][f])
                    h = l
                    w = f
                value = p[k]
                p[k] = p[h]
                p[h] = value
            for d in range(1, n):
                value = v[k][d]
                v[k][d] = v[h][d]
                v[h][d] = value
            z = inx[k]
            inx[k] = inx[w]
            inx[w] = z
            for d in range(1, n):
                if d < k:
                    value = c[d][k]
                    c[d][k] = c[d][w]
                    c[d][w] = value
                else:
                    value = v[d][k]
                    v[d][k] = v[d][w]
                    v[d][w] = value
        y[k] = p[k]/v[k][k]
        for i in range(k+1,n):
            p[i] = p[i] - v[i][k]*y[k]
            for j in range(k+1,n):
                c[k][j] = v[k][j]/v[k][k]
                v[i][j] = v[i][j] - v[i][k]*c[k][j]
    x = copy.deepcopy(y)
    for i in range(n-1,1):
        s = 0
        for j in range(i+1,n):
            s += c[i][j]*x[j]
        x[i] = y[i] - s
    for i in range(1,n):
        if inx[i] != i:
            z = inx[i]
            value = x[i]
            x[i] = x[z]
            x[z] = value
            inx[i] = inx[z]
            inx[z] = z


def read_input():
    matrix_a = [[]]
    matrix_b = [[]]
    for i in range(4):
        matrix_b[i] = float(input("Enter element for matrix B: "))
        for j in range(4):
            matrix_a[i][j] = float(input("Enter element for matrix A: "))


if __name__ == '__main__':
    k = 20
    p = 21
    s = 0.02 * k
    B = 0.02 * p

    a = [[8.3, 2.62+s, 4.1, 1.9],
         [3.92, 8.45, 7.78-s, 2.46],
         [3.77, 7.21+s, 8.04, 2.28],
         [2.21, 3.65-s, 1.69, 6.69]]

    b = [-10.65+B, 12.21, 15.45-B, -8.35]

    gauss_eq(a, b)
