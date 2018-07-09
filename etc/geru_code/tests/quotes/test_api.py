import json

import httpretty
import pytest

from tests import utils


@httpretty.activate
@pytest.mark.io
@pytest.mark.unit
@pytest.mark.parametrize('url', (
    'https://httpbin.org/ip',
    'https://abcde.com/',
))
@pytest.mark.parametrize('key', [
    None, 'quotes', 'notpresent'
])
@pytest.mark.parametrize('body, timeout, error', (
    (utils.QUOTES, 10, False),
    (utils.BLANK, 10, True),
    (utils.mockTimeout, 0, True),
))
def test_request_json(url, key, body, timeout, error):
    from geru.quotes.api import request_json
    httpretty.register_uri(
        httpretty.GET,
        url,
        body=body,
        request_timeout=timeout
    )
    response = request_json(url=url, key=key)

    # check whether the response is an error
    assert error ^ response['status']

    # if an error, the key should not be present
    # and vice versa
    assert error ^ ('error' not in response)
    assert error ^ ('data' in response)


@httpretty.activate
@pytest.mark.io
@pytest.mark.unit
def test_get_quotes():
    from geru.quotes.api import API, get_quotes
    httpretty.register_uri(
        httpretty.GET,
        uri=API,
        body=json.dumps(utils.AWS_QUOTES)
    )
    data = get_quotes()
    assert 'data' in data
    for i, v in enumerate(data['data']):
        assert utils.AWS_QUOTES['quotes'][i] == v


@httpretty.activate
@pytest.mark.parametrize('number, error', (
    (-1, False),
    (0, False),
    (5, False),
    (18, False),
    (19, True),
    (20, True),
))
def test_get_quote(number, error):
    from geru.quotes.api import API, get_quote

    if number >= len(utils.AWS_QUOTES['quotes']):
        body = {'error': 'Not Found'}
    else:
        body = {'quote': utils.AWS_QUOTES['quotes'][number]}
    httpretty.register_uri(
        httpretty.GET,
        uri=f'{API}/{number}',
        body=json.dumps(body)
    )

    data = get_quote(number)

    if error:
        assert 'data' not in data
        assert 'error' in data
    else:
        assert 'data' in data
        assert 'error' not in data
        assert utils.AWS_QUOTES['quotes'][number] == data['data']
