#!/bin/python3


def gen_C(a, b):
    '''
    Generate the union of a and b elements.
    >>> A = [2, 5, 8, 10];\
        B = [2, 2, 3, 4, 4, 20];\
        C = gen_C(A, B);\
        print(C)
    [2, 2, 2, 3, 4, 4, 5, 8, 10, 20]
    '''
    return sorted(a + b)


def gen_D(a, b):
    '''
    Generate a list with elements from b that don't exist in a.

    >>> A = [2, 5, 8, 10];\
        B = [2, 2, 3, 4, 4, 20];\
        D = gen_D(A, B);\
        print(D)
    [3, 4, 4, 20]

    '''
    return [i for i in b if i not in a]


if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True)
