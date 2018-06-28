#  -*- coding: utf-8 -*-

"""
    NOTE:
    There are many ways of solving these problems, but what we
    are looking from you is to specifically use idiomatic Python.
    Please answer each of these problems below using Python 2.7.

    If you enjoy a challenge, you can provide multiple solutions to
    these basic questions. :)
"""


"""
**Exercise 1:**
    Transform these lists (left side is INPUT, right side is OUTPUT):
    [1,2,3,1,5] → [15,11,13,12,11]
    ['a','b','c','d','e']    →   ['e','d','c','b','a']
    ['a','b','c','d','e']    →   ['a','c','e']
    ['a','b','c','d','e']    →   ['b','d']
    [11,6,10] → [11,10,6,[27]]
"""


def exercise_1():
    # Exercise 1 solution

    import functools

    a = [1, 2, 3, 1, 5]
    # [1,2,3,1,5] → [15,11,13,12,11] ##############################
    assert map(lambda x: int('1' + str(x)), a[::-1]) == [15, 11, 13, 12, 11]
    assert [int('1' + str(x)) for x in a[::-1]] == [15, 11, 13, 12, 11]
    assert map(lambda x: 10 + x, a[::-1]) == [15, 11, 13, 12, 11]
    assert [10 + x for x in a[::-1]] == [15, 11, 13, 12, 11]

    # ['a','b','c','d','e']    →   ['e','d','c','b','a'] ##############################
    a = ['a', 'b', 'c', 'd', 'e']
    assert a[::-1] == ['e', 'd', 'c', 'b', 'a']
    assert sorted(a, reverse=True) == ['e', 'd', 'c', 'b', 'a']
    a.reverse()  # last done, because it's an in place operation
    assert a == ['e', 'd', 'c', 'b', 'a']

    # ['a','b','c','d','e']    →   ['a','c','e'] ##############################
    a = ['a', 'b', 'c', 'd', 'e']
    assert a[::2] == ['a', 'c', 'e']
    assert [x for i, x in enumerate(a, 1) if i % 2 != 0] == ['a', 'c', 'e']

    # ['a','b','c','d','e']    →   ['b','d'] ##############################
    a = ['a', 'b', 'c', 'd', 'e']
    assert a[1::2] == ['b', 'd']
    assert [x for i, x in enumerate(a) if i % 2 != 0] == ['b', 'd']

    # [11,6,10] → [11,10,6,[27]] ##############################
    a = [11, 6, 10]
    a.sort(reverse=True)  # uses the list reversed everywhere here
    assert (a + [[functools.reduce((lambda x, y: x + y), a)]]) == [11, 10, 6, [27]]
    assert (a + [[sum(a)]]) == [11, 10, 6, [27]]
    a.append([sum(a)])  # last done, beause it's an in place operation
    assert a == [11, 10, 6, [27]]


"""
    **Exercise 2:**
    We have a function `complex_function` to compute certain data, printing out
    the result after the computation. This is great, but we want to add some
    functionality. We want to push to a log:
    - the time used by the function to run
    - the name of the function
    - the input values of the function.

    Note: We cannot modify the body of the original `complex_function` function.
"""


def exercise_2():
    # Exercise 2 solution

    import time
    from functools import wraps

    def profile_method(func):
        """
        Logs:
            - the time used by the function to run
            - the name of the function
            - the input values of the function.
        """
        @wraps(func)
        def wrapper(*ag, **kw):
            start_time = time.time()
            result = func(*ag, **kw)
            total_time = time.time() - start_time
            # done as prints because it's simpler
            # could've been done using the lib logging
            print('Function name: ' + func.__name__)
            print('Total runtime: ' + str(total_time))
            print('args: ' + str(ag))
            print('kwargs: ' + str(kw))
            return result
        return wrapper

    @profile_method
    def complex_function(*ag, **kw):
        # some amazing inner code
        time.sleep(1)

    complex_function(1, 2, 3, a=1, b=2)


"""
**Exercise 3:**
    Define a custom `MyDict` class that allows the following operations:
    - set/read values using both the dot notation (e.g. `mydict.name`) and
      item access notation used for dictionaries (e.g. `mydict[name]`).
      In case the mapped value is not present, returns `None`.
    - A + B addition operation:
      `MyDict` + `dict` = `MyDict`;
      `MyDict` + `MyDict` = `MyDict`;
      the result of this operation is a `MyDict` object, having all the fields
      of both dictionaries. In case of common keys between the dictionaries,
      their values need to be added/appended together (according to their type.
      For the sake of the exercise, admissible types are only
      `int` and `string`).

      Example:
      ```
      m = MyDict()
      m.a = 10
      m['b'] = 20
      print m['c']  # prints `None`
      n = {'a': 10, 'c': 15}
      print m + n  # prints `{'a': 20, 'b':20, 'c': 15}
      ```
"""


def exercise_3():
    # Exercise 3 solution

    import numbers

    class MyDict(object):

        def __new__(cls, *ag, **kw):
            if ag and len(ag) > 0:
                for k, v in ag[0].items():
                    cls._str_or_number(v)
            return super(MyDict, cls).__new__(cls, *ag, **kw)

        @classmethod
        def _str_or_number(cls, v):
            if not isinstance(v, (str, numbers.Number)):
                raise Exception('"{}" isn\'t a str or a number.'.format(v))

        def __init__(self, *ag, **kw):
            super(MyDict, self).__init__()
            self.__dict__['inner_dict'] = {}
            if ag and len(ag) > 0:
                self.__dict__['inner_dict'] = {}
                for k, v in ag[0].items():
                    self.__dict__['inner_dict'][k] = v
            self.__dict__.update(kw)

        def __add__(self, other):
            output = MyDict(self.__dict__['inner_dict'])
            for k, v in other.items():
                self._str_or_number(v)
                ref = output.get(k)
                if isinstance(v, str) or isinstance(ref, str):
                    val = str(ref or '') + str(v)
                else:
                    val = (ref or 0) + v
                output[k] = val
            return output
        __radd__ = __add__

        def __contains__(self, item):
            return item in self.__dict__['inner_dict']

        def __delitem__(self, key):
            del self.__dict__['inner_dict'][key]

        def __getitem__(self, key):
            return self.__dict__['inner_dict'].get(key)

        def __getattr__(self, attr):
            return self.__dict__['inner_dict'].get(attr)

        def __iter__(self):
            return self.__dict__['inner_dict'].__iter__()

        def __len__(self):
            return len(self.__dict__['inner_dict'])

        def __setitem__(self, attr, value):
            self._str_or_number(value)
            self.__dict__['inner_dict'][attr] = value

        def __setattr__(self, attr, value):
            self._str_or_number(value)
            self.__dict__['inner_dict'][attr] = value

        def __unicode__(self):
            skeys = sorted(self.__dict__['inner_dict'].keys())
            output = []
            for k in skeys:
                val = self.__dict__['inner_dict'][k]
                if not isinstance(val, numbers.Number):
                    val = u"'%s'" % (val)
                output.append(u'\'{}\': {}'.format(k, val))
            return u'MyDict({' + u', '.join(output) + '})'

        def __str__(self):
            skeys = sorted(self.__dict__['inner_dict'].keys())
            output = []
            for k in skeys:
                val = self.__dict__['inner_dict'][k]
                if not isinstance(val, numbers.Number):
                    val = "'%s'" % (val)
                output.append(u'\'{}\': {}'.format(k, val))
            return u'MyDict({' + ', '.join(output) + '})'

        __repr__ = __str__

        def __bool__(self):
            return bool(self.__dict__['inner_dict'])
        __nonzero__ = __bool__

        def __eq__(self, item):
            if isinstance(item, (MyDict, dict)):
                if set(item.keys()) == set(self.keys()):
                    return all(self[k] == item[k] for k in item.keys())
            return False

        def __getstate__(self):
            '''
            Pickle.
            '''
            return self.__dict__['inner_dict']

        def __setstate__(self, state):
            '''
            Unpickle.
            '''
            self.__dict__['inner_dict'] = state

        def get(self, k, default=None):
            return self.__dict__['inner_dict'].get(k, default)

        def items(self):
            return self.__dict__['inner_dict'].items()

        def keys(self):
            return self.__dict__['inner_dict'].keys()

        def values(self):
            return self.__dict__['inner_dict'].values()

    a = MyDict({'a': 1, 'b': 2})
    b = {'b': 10, 'c': '50'}
    assert type(a + b) == MyDict
    assert (a + b) == MyDict({'a': 1, 'b': 12, 'c': '50'})
    c = MyDict({'b': 10, 'c': 50})
    assert type(a + c) == MyDict
    assert (a + c) == MyDict({'a': 1, 'b': 12, 'c': 50})
    assert type(b + a) == MyDict


if __name__ == '__main__':
    print('running/"testing" exercise_1')
    exercise_1()
    print('\nrunning/"testing" exercise_2')
    exercise_2()
    print('\nrunning/"testing" exercise_3')
    exercise_3()
