import pytest

from geru.views import api
from tests import utils


class BaseListViewTest:
    __base_model_test__ = True

    view_class = None
    data = None

    def _create_data(self, database, number=1):
        from geru.models.pageviews import PageView

        database.add_all(PageView(**self.data) for _ in range(number))
        database.flush()

    def test_empty(self, database):
        info = self.view_class().get(utils.dummy_request(database))
        assert self.api_key in info.json
        assert info.status_code == 200
        assert len(info.json[self.api_key]) == 0

    def test_get_all(self, database):
        self._create_data(database, number=20)

        info = self.view_class().get(utils.dummy_request(database))
        assert self.api_key in info.json
        assert info.status_code == 200
        assert len(info.json[self.api_key]) > 0


class BaseSingleViewTest:
    __base_model_test__ = True

    view_class = None
    data = None
    oid = None

    def _create_data(self, database, number=1):
        from geru.models.pageviews import PageView

        database.add_all(PageView(**self.data) for _ in range(number))
        database.flush()

    def test_empty(self, database):
        info = self.view_class().get(
            utils.dummy_request(database), id=self.oid
        )
        assert 'error' in info.json
        assert info.json['error'] == 'Not Found'
        assert info.status_code == 404

    def test_get(self, database):
        self._create_data(database, number=20)

        info = self.view_class().get(
            utils.dummy_request(database), id=self.oid
        )
        assert self.api_key in info.json
        assert info.status_code == 200
        assert len(info.json) == 1

    def test_get_error(self, database):
        self._create_data(database, number=20)

        info = self.view_class().get(
            utils.dummy_request(database), id='-17236127356671'
        )
        assert 'error' in info.json
        assert info.json['error'] == 'Not Found'
        assert info.status_code == 404


@pytest.mark.views
@pytest.mark.unit
class TestRequestView(BaseListViewTest):
    view_class = api.RequestView
    api_key = 'requests'
    data = {
        'session_id': 'asjdkasdhjghj',
        'url': 'any.com'
    }


@pytest.mark.views
@pytest.mark.unit
class TestRequestDetailView(BaseSingleViewTest):
    view_class = api.RequestDetailView
    api_key = 'request'
    data = {
        'session_id': 'asjdkasdhjghj',
        'url': 'any.com'
    }
    oid = 1


@pytest.mark.views
@pytest.mark.unit
class TestSessionView(BaseListViewTest):
    view_class = api.SessionView
    api_key = 'sessions'
    data = {
        'session_id': 'asjdkasdhjghj',
        'url': 'any.com'
    }


@pytest.mark.views
@pytest.mark.unit
class TestSessionDetailView(BaseSingleViewTest):
    view_class = api.SessionDetailView
    api_key = 'session'
    data = {
        'session_id': 'asjdkasdhjghj',
        'url': 'any.com'
    }
    oid = 'asjdkasdhjghj'
