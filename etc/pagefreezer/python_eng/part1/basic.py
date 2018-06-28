
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
    [‘a’,’b’,’c’,’d’,’e’]    →   [‘e’,’d’,’c’,’b’,’a’]
    [‘a’,’b’,’c’,’d’,’e’]    →   [‘a’,’c’,’e’]
    [‘a’,’b’,’c’,’d’,’e’]    →   [‘b’,’d’]
    [11,6,10] → [11,10,6,[27]]
"""
# Exercise 1 solution




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
# Exercise 2 solution




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
# Exercise 3 solution


