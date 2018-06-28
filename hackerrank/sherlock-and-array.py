#!/bin/python3

values = '''10
1
1
1
2
1
3
2
1 2
3
1 4 1
3
1 5 1
1
234
1
20000
3
6 23 6
1
1'''.split('\n')


def input():
    temp = values[0]
    del values[0]
    return temp


lines = int(input())
for _ in range(lines):
    _ = input()
    inp = input().split()
    if len(inp) in (0, 1):
        print('YES')
        continue

    word = tuple(map(int, inp))
    lsum, rsum = word[0], sum(word[2:])
    for i in range(2, len(word)):
        if lsum == rsum:
            print('YES')
            break
        else:
            lsum += word[i - 1]
            rsum -= word[i]
    else:
        print('NO')
