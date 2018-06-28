#!/bin/python3

values = [
    '2',
    '8 9',
    '1 2',
    '1 3',
    '3 4',
    '3 5',
    '4 6',
    '4 8',
    '5 4',
    '6 7',
    '7 8',
    '1',
    '3 1',
    '2 3',
    '2']


def input():
    temp = values[0]
    del values[0]
    return temp


from collections import defaultdict, deque

DISTANCE = 6


def distances(graph, start, num_nodes):
    dists = defaultdict(lambda: -1)
    dists[start] = 0
    to_visit = deque([(start, i) for i in graph[start]])
    while len(to_visit) > 0:
        st, ed = to_visit.popleft()
        if dists[ed] >= 0:
            dists[ed] = min(dists[st] + DISTANCE, dists[ed])
        else:
            dists[ed] = dists[st] + DISTANCE
        to_visit.extend([(ed, i) for i in graph[ed]])
        del graph[ed]
    return dists

for _ in range(int(input().strip())):
    num_nodes, e = list(map(int, input().strip().split()))
    graph = defaultdict(set)
    for _ in range(e):
        aux = list(map(int, input().strip().split()))
        graph[aux[0]].add(aux[1])
        graph[aux[1]].add(aux[0])

    start = int(input().strip())
    ds = distances(graph, start, num_nodes)
    print(' '.join(map(
        str,
        (ds[i + 1] for i in range(num_nodes) if ds[i + 1] != 0))
    ))


'''
6 6 -1
-1 6
'''
