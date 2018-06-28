from requests import Response
from requests import Session

from settings import thread_pool


class AsyncSession(Session):
    '''
    Adapted FuturesSession from https://github.com/ross/requests-futures/
    '''

    class FetchDefaultDict(dict):
        def __init__(self, iterable=None, **kwargs):
            self._callback = kwargs.pop('_update_fetch_defaults')
            super().__init__(iterable, **kwargs)

        def __setitem__(self, key, value):
            super().__setitem__(key, value)
            self._callback()

    def __init__(self, fetch_defaults=None):
        super().__init__()
        self.executor = thread_pool

        if fetch_defaults is None:
            fetch_defaults = {}

        self._fetch_defaults = self.FetchDefaultDict(
            fetch_defaults,
            _update_fetch_defaults=lambda: self._update_fetch_defaults()
        )
        self._update_fetch_defaults()

    def _update_fetch_defaults(self):
        for key, value in self._fetch_defaults.items():
            if hasattr(self, key):
                if isinstance(getattr(self, key), dict):
                    setattr(self, key, getattr(self, key).update(value))
                elif isinstance(getattr(self, key), (tuple, list)):
                    setattr(self, key, getattr(self, key) + value)
                else:
                    setattr(self, key, value)

    @property
    def fetch_defaults(self):
        return self._fetch_defaults

    @fetch_defaults.setter
    def fetch_defaults(self, value):
        self._fetch_defaults = value
        self._update_fetch_defaults()

    def request(self, *args, **kwargs):
        """Maintains the existing api for Session.request.

        Used by all of the higher level methods, e.g. Session.get.

        The background_callback param allows you to do some processing on the
        response in the background, e.g. call resp.json() so that json parsing
        happens in the background thread.
        """
        sup = super().request

        background_callback = kwargs.pop('background_callback', None)
        if background_callback:
            def wrap(*args_, **kwargs_):
                resp = sup(*args_, **kwargs_)
                background_callback(self, resp)
                return resp

            sup = wrap

        def wrap_response_adapter(*args_, **kwargs_):
            resp = sup(*args_, **kwargs_)
            if isinstance(resp, Response):
                # adapt Response fields to Tornado variant
                resp.effective_url = resp.url
                resp.body = resp.content
                resp.code = resp.status_code
            return resp

        func = wrap_response_adapter

        return self.executor.submit(func, *args, **kwargs)
