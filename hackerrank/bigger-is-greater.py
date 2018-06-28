class MinBigger():

    indexes = None
    bigger = None

    def __init__(self, bigger):
        self.bigger = bigger

    def min_bigger(self, bigger, index):
        value = bigger[index][:]
        try:
            a = min(filter(lambda x: x > value, bigger))
        except ValueError:
            return -1
        return self.bigger.rindex(a)

    def bigger_greater(self):
        bigger = list(self.bigger)

        for piece in range(len(bigger) - 2, -1, -1):
            self.indexes = {a: self.bigger.rindex(a) for a in bigger}

            for i in range(len(bigger[piece:]) - 1, -1, -1):
                min_i = self.min_bigger(bigger[piece:], i)
                if min_i > piece + i:
                    bigger[piece + i], bigger[min_i] = bigger[min_i], bigger[piece + i]
                    bigger[piece + i + 1:] = sorted(bigger[piece + i + 1:])
                    return ''.join(bigger)
        return 'no answer'


def min_bigger(bigger, index):
    value = bigger[index - 1][:]
    try:
        a = min(filter(lambda x: x > value, bigger[index:]))
    except ValueError:
        return -1
    r_index = len(bigger[index:]) - bigger[index:][::-1].index(a) - 1
    return r_index + index


def bigger_greater(bigger):
    bigger = list(bigger)
    for i in range(len(bigger) - 1, 0, -1):
        if bigger[i - 1] < bigger[i]:
            index = min_bigger(bigger, i)
            bigger[i - 1], bigger[index] = bigger[index], bigger[i - 1]
            bigger[i:] = sorted(bigger[i:])
            return ''.join(bigger)
    return 'no answer'


if __name__ == "__main__":
    with open('bigger-is-greater-input.txt', 'r') as inp:
        with open('bigger-is-greater-output.txt', 'r') as out:
            lines = int(inp.readline().strip())
            for example, expected in zip(inp, out):
                example = example.strip()
                expected = expected.strip()
                output = bigger_greater(example)
                if output != expected:
                    print(example, output, expected)
