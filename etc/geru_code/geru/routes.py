from geru.views import api, default, errors


def includeme(config):
    config.add_static_view('static', 'static/', cache_max_age=3600)

    api.includeme(config)
    default.includeme(config)
    errors.includeme(config)
