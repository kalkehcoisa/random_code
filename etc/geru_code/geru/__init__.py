from pyramid.config import Configurator
import pyramid.tweens
from pyramid_nacl_session import EncryptedCookieSessionFactory

from geru import cache


def main(global_config, **settings):
    """
    This function returns a Pyramid WSGI application.
    """

    # this call inits/enable/disable the cache
    cache.refresh()

    config = Configurator(settings=settings)

    # session configuration
    hex_secret = bytes.fromhex(settings['geru.session_secret'].strip())
    factory = EncryptedCookieSessionFactory(hex_secret)  # other config ad lib.
    config.set_session_factory(factory)

    # tween to handle the session and track the urls visited
    config.add_tween(
        'geru.tweens.user_tracker_tween',
        over=pyramid.tweens.MAIN
    )

    # adding here the packages used in all envs
    config.include('pyramid_jinja2')
    config.include('pyramid_restful')
    config.include('.models')
    config.include('.routes')

    config.scan()
    return config.make_wsgi_app()
