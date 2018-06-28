#!/bin/python3

values = '''1
5 7
3 3 9 9 5
'''.split('\n')


def input():
    temp = values[0]
    del values[0]
    return temp


cases = int(input())
for _ in range(cases):
    length, mod = map(int, input().split())
    mods = list(map(lambda x: int(x) % mod, input().split()))

    max_mod = max(mods)
    for leng in range(2, length + 1):
        for start in range(length - leng + 1):
            mods[start] = sum(mods[start:start + leng]) % mod
            max_mod = max(mods[start], max_mod)
    print(max_mod)
