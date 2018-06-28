# -*- coding: utf-8 -*-

import uuid

import nose
import webtest

BASE_URL = 'http://localhost:8000/'


def test_home():
    '''
    Check if the / is accessible.
    '''
    api = webtest.TestApp(BASE_URL)
    r = api.get('/')
    assert r.json_body['status']


def test_graph():
    '''
    Check if the /graph is accessible.
    '''
    api = webtest.TestApp(BASE_URL)
    r = api.get('/graph')
    assert 'status' in r.json_body


def test_register_graph():
    '''
    Check if it's possible to register a new graph.
    '''
    api = webtest.TestApp(BASE_URL)

    graph_input = '''A B 10
B D 15
A C 20
C D 30
B E 50
D E 30'''
    name = str(uuid.uuid4())
    r = api.post(
        '/graph',
        {'graph': graph_input, 'name': name})

    assert 'status' in r
    assert r.json_body['status']


def test_reregister_graph():
    '''
    Try to register two graphs with the same name.
    '''
    api = webtest.TestApp(BASE_URL)

    graph_input = '''A B 10
B D 15
A C 20
C D 30
B E 50
D E 30'''
    name = str(uuid.uuid4())
    r = api.post(
        '/graph',
        {'graph': graph_input, 'name': name})
    assert 'status' in r

    r = api.post(
        '/graph',
        {'graph': graph_input, 'name': name})
    assert 'status' in r
    assert not r.json_body['status']


def test_calc_best_route():
    '''
    Check if the best route calculation is working properly.
    '''
    api = webtest.TestApp(BASE_URL)

    graph_input = '''A B 10
B D 15
A C 20
C D 30
B E 50
D E 30'''
    name = str(uuid.uuid4())
    r = api.post(
        '/graph',
        {'graph': graph_input, 'name': name})
    assert 'status' in r
    assert r.json_body['status']

    r = api.get(
        '/graph',
        {'name': name,
         'start': 'A',
         'target': 'D',
         'autonomy': 10,
         'gas_price': 2.50})

    assert r.json_body['status']
    assert r.json_body['cost'] == 6.25
    assert r.json_body['route'] == ['A', 'B', 'D']

if __name__ == '__main__':
    nose.main()
