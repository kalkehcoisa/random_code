#!/bin/python3

import functools


def factorial(num):
    '''
    A method that receives a number and calculate its factorial.
    Must receive a non negative integer.

    Doctests for checking if everything is fine.

    >>> factorial(0)
    1
    >>> factorial(1)
    1
    >>> factorial(2)
    2
    >>> factorial(3)
    6
    >>> factorial(4)
    24
    >>> factorial(5)
    120
    >>> factorial(5.5)
    Traceback (most recent call last):
        ...
    ValueError: num (5.5) must be a positive integer

    >>> factorial(-5.5)
    Traceback (most recent call last):
        ...
    ValueError: num (-5.5) must be >= 0

    >>> factorial(10)
    3628800

    '''
    if num < 0:
        raise ValueError('num ({num}) must be >= 0'.format(num=num))
    if int(num) != num:
        raise ValueError(
            'num ({num}) must be a positive integer'.format(num=num))

    if num in (0, 1):
        return 1
    else:
        # uses the reduce function to multiple the numbers generated
        # by the range generator
        return functools.reduce(lambda n1, n2: n1 * n2, range(1, num + 1))


if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True)
