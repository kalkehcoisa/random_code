from collections import defaultdict


def MostPopularNumber(numbers, arr_len):
    if len(numbers) == 0:
        return None
    aux = defaultdict(int)
    for i in numbers:
        aux[i] += 1
    aux = filter(lambda x: x[1] == max(aux.values()), aux.items())
    aux = sorted(aux, key=lambda x: x[0])
    return aux[0]

MostPopularNumber([14, 14, 2342, 2342, 2342, 3000, 3000, 3000], 5)
MostPopularNumber([34, 31, 31, 34, 77, 82], 5)
MostPopularNumber([92, 101, 102, 101, 102, 525, 88], 7)
MostPopularNumber([66], 1)
MostPopularNumber([14, 14, 2342, 2342, 2342, 3000, 3000, 3000, 3000], 5)
