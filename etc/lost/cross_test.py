import sys

"""
* Complete the function below.
* DO NOT MODIFY CODE OUTSIDE THIS FUNCTION!
"""


def twins(a, b):
    answers = []
    ref = b if len(a) > len(b) else a
    for i, _ in enumerate(ref):
        check = set(a[i][::2]) == set(b[i][::2]) and set(a[i][1::2]) == set(b[i][1::2])
        answers.append('Yes' if check else 'No')
    answers.extend(['No'] * (len(a) - len(b)))
    return answers


"""
* DO NOT MODIFY CODE BELOW THIS POINT!
"""


def main():
    # data = sys.stdin.readlines()
    data = '''10
cdabe
dcbae
abcdefhg
4
5
6
7
8
9
10
2
abcde
abcde'''.split('\n')

    pos = 0

    a = []
    b = []

    for a_i in range(pos + 1, int(data[pos]) + 1):
        a.append(data[a_i])

    pos = len(a) + 1

    for b_i in range(pos + 1, int(data[pos]) + pos + 1):
        b.append(data[b_i])

    result = twins(a, b)

    for i, val in enumerate(result):
        print(i, val)
    print(result)


main()
