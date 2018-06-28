#!/bin/python3

mat = [
    [1, 1, 1, 0, 0, 0],
    [0, 1, 0, 0, 0, 0],
    [1, 1, 1, 0, 0, 0],
    [0, 0, 2, 4, 4, 0],
    [0, 0, 0, 2, 0, 0],
    [0, 0, 1, 2, 4, 0],
]


def soma(mat, x, y):
    return sum(mat[x][y:y + 3]) + mat[x + 1][y + 1] + sum(mat[x + 2][y:y + 3])

m = max(soma(mat, x, y) for x in range(len(mat) - 2) for y in range(len(mat[x]) - 2))
print(m)
