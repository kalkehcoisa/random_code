#!/bin/python3

a1, a2, n = list(map(int, input().strip().split()))


def mod_fibo(a1, a2, n):
	for _ in range(1, n // 2 + n % 2):
		a1 = a2 ** 2 + a1
		a2 = a1 ** 2 + a2

	return a1 if n % 2 == 1 else a2

mod_fibo(a1, a2, n)



'''
So, if the first two terms of the series are 0 and 1:
the third term = 1 ** 2 + 0 = 1
fourth term = 1 ** 2 + 1 = 2
fifth term = 2 ** 2 + 1 = 5
'''