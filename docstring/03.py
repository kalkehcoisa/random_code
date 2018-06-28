#!/bin/python3

from collections import UserDict


class Professions(UserDict):
    '''
    A class to store and retrieve professions associated with people.
    Made using UserDict to hide the dict attributes and avoid conflict.

    Has the same __init__ method as dict.

    Doctests
    >>> profs = Professions({\
        'Marion': 'Engineer',\
        'James': 'Doctor',\
        'Frederick': 'Accountant',\
        'John': 'Lawyer',\
    });\
    profs.get('Marion');\
    profs.get('James');
    'Engineer'
    'Doctor'

    >>> profs = Professions({\
        'Marion': 'Engineer',\
        'James': 'Doctor',\
        'Frederick': 'Accountant',\
        'John': 'Lawyer',\
    });\
    profs.get('Jayme') is None
    True

    >>> profs = Professions({\
        'Marion': 'Engineer',\
        'James': 'Doctor',\
        'Frederick': 'Accountant',\
        'John': 'Lawyer',\
    });\
    profs.add('Jayme', 'Systems Analyst');\
    profs.get('Jayme')
    'Systems Analyst'

    >>> profs = Professions({\
        'Marion': 'Engineer',\
        'James': 'Doctor',\
        'Frederick': 'Accountant',\
        'John': 'Lawyer',\
    });\
    profs['Jayme'] = 'Systems Analyst';\
    profs['Jayme']
    'Systems Analyst'

    '''

    def get(self, name):
        return self.data.get(name, None)

    def __get__(self, name):
        return self.data.get(name, None)

    def add(self, name, profession):
        self.data[name] = profession

    def __set__(self, name, profession):
        self.data[name] = profession


if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True)
