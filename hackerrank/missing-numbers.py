#!/bin/python3

values = '''10
203 204 205 206 207 208 203 204 205 206
13
203 204 204 205 206 207 205 208 203 206 205 206 204
'''.split('\n')
# 204 205 206


def input():
    temp = values[0]
    del values[0]
    return temp


from collections import Counter


_, first = input(), Counter(map(int, input().split()))
_, second = input(), Counter(map(int, input().split()))
for key in sorted((second - first).keys()):
    print(key, end=' ')
