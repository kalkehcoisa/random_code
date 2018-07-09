from pyramid import testing
import pytest


from tests import utils
from geru.views import errors


@pytest.mark.views
@pytest.mark.unit
def test_notfound_view(database):
    config = testing.setUp(package='geru')
    config.include('pyramid_jinja2')
    from geru.routes import includeme
    includeme(config)

    info = errors.notfound_view(
        utils.dummy_request(database)
    )
    # Response(html, headers={'status': '404 Not Found'})
    assert info.status_code == 404
    assert 'Page Not Found' in info.body.decode('utf-8')

    testing.tearDown()
