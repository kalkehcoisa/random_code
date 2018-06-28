#!/bin/python3

values = [
    '5',
    '2 4 6 8 3 5 1'
]

'''
2 4 6 8 8
2 4 6 6 8
2 4 4 6 8
2 3 4 6 8
'''
(3, ['2', '4', '6', '8', '8'])
(3, ['2', '4', '6', '6', '8'], '6')
(2, ['2', '4', '4', '6', '8'], '4')
(1, ['2', '2', '4', '6', '8'], '2')


def input():
    temp = values[0]
    del values[0]
    return temp


length = input().strip()
arr = list(map(int, input().strip().split()))

val = None
for i in range(1, len(arr)):
    if arr[i] < arr[i - 1]:
        val = arr[i]
        arr[i] = arr[i - 1]
        j = i - 1
        print(' '.join(map(str, arr)))
        while arr[j] > val and j > -1:
            if j - 1 < 0 or arr[j - 1] <= val:
                arr[j] = val
                print(' '.join(map(str, arr)))
                break
            elif arr[j - 1] > val:
                arr[j] = arr[j - 1]
                print(' '.join(map(str, arr)))
            j -= 1
