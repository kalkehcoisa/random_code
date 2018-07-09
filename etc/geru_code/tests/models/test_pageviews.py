import pytest


@pytest.mark.models
@pytest.mark.unit
@pytest.mark.incremental
class TestPageView:
    model = None
    data = {
        'session_id': 'asjdkasdhjghj',
        'url': 'any.com'
    }

    def test_create(self, database):
        from geru.models.pageviews import PageView
        page = PageView(**self.data)
        database.add(page)
        database.flush()

        assert page.id is not None
        assert page.date is not None
        assert database.query(PageView).count() == 1

    def test_to_dict(self, database):
        from geru.models.pageviews import PageView
        page = database.query(PageView).first()
        d = page.to_dict()
        for k in self.data.keys():
            assert d[k] == self.data[k]

        d = page.to_dict(exclude=['session_id'])
        assert 'session_id' not in d
