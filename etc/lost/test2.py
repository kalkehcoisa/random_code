# you can write to stderr for debugging purposes, e.g.
# sys.stderr.write("this is a debug message\n")


def blocks(A, size):
    for i in range(0, len(A), size):
        yield A[i:i + size]


def solution(A, K):
    if len(A) < K:
        K = len(A)

    max_width = max(len(repr(i)) for i in A)
    blocked = list(blocks(A, K))

    print((('+' + '-' * max_width) * len(blocked[0])) + '+')
    for line in blocked:
        for i, x in enumerate(line, 1):
            print('|' + repr(x).rjust(max_width), end='')
        else:
            print('|')
        print((('+' + '-' * max_width) * len(line)) + '+')


if __name__ == '__main__':
    solution([4, 35, 80, 123, 12345, 44, 8, 5], 10)
    solution([4, 35, 80, 123, 12345, 44, 8, 5, 24, 3], 4)
    solution([4, 35, 80, 123, 12345, 44, 8, 5, 24, 3, 22, 35], 4)
    print('')
