def count_opened(st, end):
    if end == 0:
        return 0

    op = 0
    for i, c in enumerate(t[:end + 1]):
        if c == '[':
            op += 1
        elif c == ']':
            op -= 1
    return op


def search_closing(st, start):
    target = opened = count_opened(st, start)
    for i, c in enumerate(st[start:]):
        if c == '[':
            opened += 1
            if target == opened:
                return start + i
        elif c == ']':
            opened -= 1
            if target == opened:
                return start + i


t = '[ABC[23]][89]'
index = 9

for index, eoutput in ((0, 8), (4, 7), (9, 12)):
    output = search_closing(t, index)
    print('{} - {}: {}'.format(t, index, output))
    assert output == eoutput
