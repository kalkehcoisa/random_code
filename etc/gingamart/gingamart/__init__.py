# -*- coding: utf-8 -*-

import json
import os
import re

import falcon
import numpy as np
from playhouse.kv import PickleField
import peewee
from scipy.sparse.csgraph import dijkstra
from scipy.sparse import coo_matrix


ROOT_PATH = os.path.dirname(os.path.realpath(__file__))
DB_FILE = os.path.join(ROOT_PATH, 'dados.db')
db = peewee.SqliteDatabase(DB_FILE, threadlocals=True)


class BaseModel(peewee.Model):
    class Meta:
        database = db


class Map(BaseModel):
    '''
    Stores a preprocessed graph.
    `cols` and `rows` are lists holding coordinates
    for `data`.
    For example, cols[0], rows[0], data[0] defines
    the first point.
    '''
    name = peewee.CharField(primary_key=True)
    cols = PickleField()
    rows = PickleField()
    labels = PickleField()
    data = PickleField()


def clean_raw_graph(raw_graph):
    '''
    Removes all non alphanumerical characters
    from the string.
    '''
    cleaned = []
    for item in raw_graph.split(u'\n'):
        rx = re.compile('\W+')
        item = rx.sub(' ', item)
        rea = re.compile(' {2,}')
        item = rea.sub(' ', item).strip()
        cleaned.append(item)
    return u'\n'.join(cleaned)


def preprocess_graph(graph_input):
    '''
    Preprocess the graph_input and returns the `rows`, `cols` and `data`
    needed to build a graph as a sparse matrix in scipy.
    And a translate table `labels` (to be able to convert point numbers
    to their original names).
    '''

    rows = []     # row coords
    cols = []     # col coords
    data = []    # the distance between row and col
    labels = {}  # translates destinies to coords
    counter = 0
    for edge in graph_input.split('\n'):
        item = edge.split(' ')
        if item[0] not in labels:
            labels[item[0]] = counter
            counter += 1
        rows.append(labels[item[0]])
        if item[1] not in labels:
            labels[item[1]] = counter
            counter += 1
        cols.append(labels[item[1]])
        data.append(float(item[2]))

    return rows, cols, labels, data


def build_graph(cols, rows, data):
    '''
    Build the graph as a coordinated sparse matrix.
    '''

    i = len(data)
    rows = np.array(rows)
    cols = np.array(cols)
    data = np.array(data)
    return coo_matrix((data, (rows, cols)), shape=(i, i))


def find_best_route(graph, labels, start, target):
    '''
    Find the best route using Dijkstra algorithm
    and a sparse matrix.
    Returns the minimum distance and the best route.
    '''

    # search for the best route
    i1 = labels[start]
    i2 = labels[target]
    distances, predecessors = dijkstra(
        graph, indices=i1,
        return_predecessors=True)

    # generate a list as the best route
    reverse_labels = {labels[k]: k for k in labels.keys()}
    path = []
    i = i2
    while i != i1:
        path.insert(0, reverse_labels[i])
        i = predecessors[i]
    path.insert(0, reverse_labels[i1])

    return (distances[i2], path)


class GraphResource():
    def __init__(self, db):
        self.db = db

    def on_get(self, req, resp):
        '''
        Calculates the best route of graph.
        '''

        graph_name = req.params.get('name')
        start = req.params.get('start')
        target = req.params.get('target')
        autonomy = req.params.get('autonomy')
        gas_price = req.params.get('gas_price')

        try:
            mapp = Map.get(Map.name == graph_name)

            graph = build_graph(mapp.cols, mapp.rows, mapp.data)
            distance, route = find_best_route(
                graph, mapp.labels, start, target)

            cost = (float(gas_price)/float(autonomy)) * float(distance)

            resp.status = falcon.HTTP_200
            resp.body = json.dumps({
                'status': True,
                'cost': cost,
                'route': route})
        except peewee.DoesNotExist:
            message = u'The required graph {name} doesn\'t exist!'
            resp.status = falcon.HTTP_200
            resp.body = json.dumps({
                'status': False,
                'message': message.format(name=graph_name)})
            return resp

    def on_post(self, req, resp):
        '''
        Register the graph.
        '''
        raw_graph = req.params.get('graph')
        graph_name = req.params.get('name')

        temp = raw_graph.split('\n')[::]
        # cleans the graph from bad characters
        raw_graph = clean_raw_graph(raw_graph)

        graph = Map.select().where(Map.name == graph_name)
        if graph.count() == 0:
            rows, cols, labels, data = preprocess_graph(raw_graph)
            graph = Map.create(
                name=graph_name,
                cols=cols, rows=rows,
                labels=labels, data=data)

            resp.status = falcon.HTTP_200
            message = u'Graph {name} registered succesfully!'
            resp.body = json.dumps({
                'status': True,
                'message': message.format(name=graph_name),
                'temp': temp})
        else:
            graph = graph.get()

            resp.status = falcon.HTTP_200
            message = u'Graph {name} already registered!'
            resp.body = json.dumps({
                'status': False,
                'message': message.format(name=graph_name),
                'temp': temp})


class HomeResource():
    def __init__(self, db):
        self.db = db

    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.body = json.dumps({'status': True})

app = falcon.API()
db.connect()
home = HomeResource(db)
graph = GraphResource(db)
app.add_route('/', home)
app.add_route('/graph', graph)

db.create_tables([Map], safe=True)
