import json

import httpretty
import pytest

from geru.views import default
from tests import utils


@httpretty.activate
@pytest.mark.views
@pytest.mark.unit
def test_home(database):
    info = default.home(
        utils.dummy_request(database)
    )
    assert isinstance(info, dict)
    assert len(info) == 0


@httpretty.activate
@pytest.mark.views
@pytest.mark.unit
def test_quotes(database):
    from geru.quotes.api import API
    httpretty.register_uri(
        httpretty.GET,
        uri=API,
        body=json.dumps(utils.AWS_QUOTES)
    )
    info = default.quotes(
        utils.dummy_request(database)
    )
    assert isinstance(info, dict)
    assert 'quotes' in info
    assert len(info['quotes']) > 0


@httpretty.activate
@pytest.mark.views
@pytest.mark.unit
def test_quote_rnd(database):
    from geru.quotes.api import API
    httpretty.register_uri(
        httpretty.GET,
        uri=API,
        body=json.dumps(utils.AWS_QUOTES)
    )
    info = default.quote_rnd(
        utils.dummy_request(database)
    )
    assert isinstance(info, dict)
    assert 'quote' in info
    assert len(info['quote']) > 0

    infos = set(
        default.quote_rnd(
            utils.dummy_request(database))['quote']
        for i in range(100)
    )
    assert len(infos) > 1


@httpretty.activate
@pytest.mark.views
@pytest.mark.unit
def test_quote(database):
    from geru.quotes.api import API
    qid = 5
    httpretty.register_uri(
        httpretty.GET,
        uri=API + f'/{qid}',
        body=json.dumps({'quote': utils.AWS_QUOTES['quotes'][qid]})
    )
    req = utils.dummy_request(database)
    req.matchdict = {'qid': qid}
    info = default.quote(req)

    assert isinstance(info, dict)
    assert 'quote' in info
    assert info.get('error') is None
    assert len(info['quote']) > 0
