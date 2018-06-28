#!/bin/python3

values = [
    '4 4 2',
    '1 2 3 4',
    '5 6 7 8',
    '9 10 11 12',
    '13 14 15 16']


def input():
    temp = values[0]
    del values[0]
    return temp


def print_matrix(mat):
    for line in mat:
        print(line)


def move_left(matrix, line, incomming=None):
    overflow = matrix[line][0]
    matrix[line][0] = matrix[line][-1]
    for i in range(len(matrix[line])):
        matrix[line][i - 1] = matrix[line][i]
        print(i, matrix[line][i])
    if incomming:
        matrix[line][-1] = incomming
    else:
        matrix[line][-1] = -1
    return overflow


def move_down(matrix, column, incomming=None):
    overflow = matrix[len(matrix) - 1][column]
    # matrix[0][column] = matrix[-1][column]
    for i in range(len(matrix) - 1, -1, -1):
        matrix[i][column] = matrix[i - 1][column]
    if incomming:
        matrix[0][column] = incomming
    else:
        matrix[0][column] = -1
    return overflow


m, n, r = map(int, input().strip().split())
matrix = [[int(i) for i in input().strip().split()] for k in range(m)]
print_matrix(matrix)

print(move_left(matrix, 0))

print_matrix(matrix)
