#!/bin/python3

from collections import deque


class Person:
    '''
    A class representing a person.
    '''
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name


class PeopleLine:
    '''
    This class represents people waiting in line
    to talk to a line operator.

    The attribute `line` when initialized holds a
    collections.deque, that is a list optimized
    for pushes and pops at its ends: excelent for lines
    and stacks.

    `Params:`
    - *people*: an iterable filled with Person objects.

    Doctests:
    >>> line = PeopleLine(people=[Person('José'), Person('Luiz'), Person('Joana')]).proccess()
    Person (José) has been attended
    >>> line = PeopleLine(people=[Person('José'), Person('Luiz'), Person('Joana')]).add(Person('Juan'))
    Person (Juan) has arrived
    >>> PeopleLine(people=[Person('José'), Person('Luiz'), Person('Joana')]).line
    deque([José, Luiz, Joana])
    >>> PeopleLine(people=[Person('José'), Person('Luiz'), Person('Joana')]).add(Person('Juan')).line
    Person (Juan) has arrived
    deque([José, Luiz, Joana, Juan])
    '''

    line = None

    def __init__(self, people):
        self.line = deque(people)

    def add(self, person):
        self.line.append(person)
        print('Person ({p}) has arrived'.format(p=person))
        return self

    def proccess(self):
        p = self.line.popleft()
        print('Person ({p}) has been attended'.format(p=p))
        return self

if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True)
