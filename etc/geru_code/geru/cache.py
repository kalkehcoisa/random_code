import hashlib
import inspect
import os

from dogpile.cache import make_region

PATH = os.path.dirname(os.path.realpath(__file__))
FILE_CACHING_BACKEND = 'dogpile.cache.dbm'

CACHE_FILES = set()


def ignore_args_key_generator(ignore_args_names=None, compression_length=16):
    def function_key_generator(namespace, fn, to_str=str):
        '''
        Return a function that generates a string
        key, based on a given function as well as
        arguments to the returned function itself.

        This is used by :meth:`.CacheRegion.cache_on_arguments`
        to generate a cache key from a decorated function.

        It can be replaced using the ``function_key_generator``
        argument passed to :func:`.make_region`.
        '''

        if namespace is None:
            namespace = '%s:%s' % (fn.__module__, fn.__name__)
        else:
            namespace = '%s:%s|%s' % (fn.__module__, fn.__name__, namespace)

        w_args = inspect.getargspec(fn)
        has_self = w_args[0] and w_args[0][0] in ('self', 'cls')

        def generate_simple_hash(key):
            cl = compression_length
            a = str(key).encode('utf-8')
            return '{0:0>8d}'.format(
                int(hashlib.sha1(a).hexdigest(), 16) % (10 ** cl))

        def generate_key(*args, **kw):
            args = list(args)
            if has_self:
                args = args[1:]

            if kw:
                inserts = sorted([
                    (k, w_args.args.index(k))
                    for k in kw.keys()], key=lambda i: i[1])
                args.extend([kw[i[0]] for i in inserts])

            if ignore_args_names:
                rev_ag_index = reversed([
                    w_args.args.index(ag)
                    for ag in ignore_args_names if ag in w_args.args])
                for i in rev_ag_index:
                    del args[i]

            return namespace + '|' + '-'.join(map(generate_simple_hash, args))

        return generate_key
    return function_key_generator


short_cache = None


def refresh(disable=False):
    """
    This method enables/disables the cache.
    """

    if disable:
        FILE_CACHING_BACKEND = 'dogpile.cache.null'
    else:
        FILE_CACHING_BACKEND = 'dogpile.cache.dbm'

    global short_cache
    short_cache = make_region(
        function_key_generator=ignore_args_key_generator()
    ).configure(
        FILE_CACHING_BACKEND,
        arguments={
            'filename': os.path.join(PATH, 'short_cache.dbm'),
            'rw_lockfile': False,
            'dogpile_lockfile': False,
        },
        expiration_time=60,
        replace_existing_backend=True,
    )
    CACHE_FILES.add(os.path.join(PATH, 'short_cache.dbm'))
