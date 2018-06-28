#!/bin/python3

values = [
    '1',
    '4 4',
    '1 2 24',
    '1 4 20',
    '3 1 3',
    '4 3 12',
    '1']

values = [
    '1',
    '10 8',
    '1 2 24',
    '1 4 20',
    '3 1 3',
    '4 3 12',
    '4 5 12',
    '5 6 12',
    '6 7 12',
    '7 8 12',
    '1']

with open('./dijkstrashortreach-input.txt', 'r') as file:
    values = file.read().split('\n')


def input():
    temp = values[0]
    del values[0]
    return temp


from collections import defaultdict, deque


def distances(graph, start, num_nodes):
    dists = defaultdict(lambda: -1)
    dists[start] = 0
    to_visit = deque([(start, i[0], i[1]) for i in graph[start]])
    while len(to_visit) > 0:
        st, ed, distance = to_visit.popleft()
        if ed == start:
            continue

        if dists[ed] > 0:
            dists[ed] = min(dists[st] + distance, dists[ed])
        else:
            dists[ed] = dists[st] + distance
        to_visit.extend([(ed, i[0], i[1]) for i in graph[ed]])
        del graph[ed]
        print(ed, dists)
    return dists

for _ in range(int(input().strip())):
    num_nodes, e = list(map(int, input().strip().split()))
    graph = defaultdict(set)

    for _ in range(e):
        aux = list(map(int, input().strip().split()))
        graph[aux[0]].add((aux[1], aux[2]))
        graph[aux[1]].add((aux[0], aux[2]))

    for i in graph.keys():
        graph[i] = sorted(graph[i])
    start = int(input().strip())
    ds = distances(graph, start, num_nodes)
    print(' '.join(map(
        str,
        (ds[i + 1] for i in range(num_nodes) if i + 1 != start))
    ))


'''
24 3 15
'''
