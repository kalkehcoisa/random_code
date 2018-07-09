import transaction

from pyramid import testing
import pytest


def pytest_sessionstart(session):
    """ before session.main() is called. """

    # disable the caching around the system
    # for properly testing
    from geru import cache
    cache.refresh(disable=True)


def pytest_sessionfinish(session, exitstatus):
    """ whole test run finishes. """
    pass


@pytest.yield_fixture(autouse=True, scope='class')
def database(request):
    '''
    Creates an in memory database for testing.
    '''

    from geru.models import meta
    from geru.models import (
        get_engine,
        get_session_factory,
        get_tm_session,
    )

    config = testing.setUp(settings={
        'sqlalchemy.url': 'sqlite:///:memory:'
    })
    config.include('geru.models')
    settings = config.get_settings()
    engine = get_engine(settings)
    meta.Base.metadata.create_all(engine)
    session_factory = get_session_factory(engine)
    session = get_tm_session(session_factory, transaction.manager)

    def tear_down():
        testing.tearDown()
    request.addfinalizer(tear_down)

    return session
