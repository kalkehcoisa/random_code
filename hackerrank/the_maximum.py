#!/bin/python3

import codecs

with codecs.open('input01.txt', 'r') as file:
    inputs = file.read().split('\n')
'''
2617065 172083036
1274115 193037987
2202862 163398048
2454939 240462364
3239908 186256172
2486039 202399661
1092777 137409985
962621 135978139
3020911 224370860
1755033 158953999
'''


def input():
    temp = inputs[0]
    del inputs[0]
    return temp


from itertools import accumulate
import operator


def max_subarray(arr):
    max_ending_here = max_so_far = arr[0]
    for x in arr[1:]:
        max_ending_here = max(x, max_ending_here + x)
        max_so_far = max(max_so_far, max_ending_here)
    return max_so_far


for _ in range(int(input().strip())):
    arr_l = input().strip()
    arr = list(map(int, input().strip().split()))

    sub_arr = max_subarray(arr)
    if any(map(lambda x: x > 0, arr)):
        sub_rdm = sum(filter(lambda x: x > 0, arr))
    else:
        sub_rdm = max(arr)

    print(sub_arr, sub_rdm)
