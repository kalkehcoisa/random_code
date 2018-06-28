#!/bin/python3

values = '''SHINCHAN
NOHARAAA
'''.split('\n')

values = '''ELGGYJWKTDHLXJRBJLRYEJWVSUFZKYHOIKBGTVUTTOCGMLEXWDSXEBKRZTQUVCJNGKKRMUUBACVOEQKBFFYBUQEMYNENKYYGUZSP
FRVIFOVJYQLVZMFBNRUTIYFBMFFFRZVBYINXLDDSVMPWSQGJZYTKMZIPEGMVOUQBKYEWEYVOLSHCMHPAZYTENRNONTJWDANAMFRX
'''.split('\n')


def input():
    temp = values[0]
    del values[0]
    return temp


import functools


str1 = input()
str2 = input()


# elimina os caracteres inuteis
for k in list(set(str1) - set(str2)):
    str1 = str1.replace(k, '')
for k in list(set(str2) - set(str1)):
    str2 = str2.replace(k, '')


@functools.lru_cache(maxsize=None)
def ocurrences(ch, string):
    return [i for i, letter in enumerate(string) if letter == ch]


@functools.lru_cache(maxsize=None)
def common_child_recursive(str_in1, str_in2):
    len1 = len(str_in1)
    if len(str_in2) == 0 or len1 == 0:
        return 0

    max_len = int(str_in1[0] in str_in2)
    if len1 > 1:
        for start, key in enumerate(str_in1):
            for i in ocurrences(key, str_in2):
                sub_length = common_child_recursive(
                    str_in1[start + 1:], str_in2[i + 1:])
                max_len = max(max_len, sub_length + 1)
    return max_len


def common_child(str1, str2):
    lengths = [[0 for j in range(len(str2) + 1)] for i in range(len(str1) + 1)]
    for i, x in enumerate(str1):
        for j, y in enumerate(str2):
            if x == y:
                lengths[i + 1][j + 1] = lengths[i][j] + 1
            else:
                lengths[i + 1][j + 1] = max(
                    lengths[i + 1][j], lengths[i][j + 1])

    return lengths[-1][-1]


print(common_child(str1, str2))
