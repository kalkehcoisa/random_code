import random

from pyramid.view import view_config

from geru.quotes import get_quote, get_quotes


def includeme(config):
    config.add_route('home', '/')
    config.add_route('quotes', '/quotes/')
    config.add_route('quote_rnd', '/quotes/random/')
    config.add_route('quote', '/quotes/{qid:\d+}/')


@view_config(
    renderer='geru:templates/home.jinja2',
    route_name='home'
)
def home(request):
    """
    Simply the home page.
    """
    return {}


@view_config(
    renderer='geru:templates/quotes.jinja2',
    route_name='quotes'
)
def quotes(request):
    """
    View that lists all the quotes.
    """
    data = get_quotes()
    quotes = error = None
    if data['status']:
        quotes = data['data']
    else:
        error = data['error']
    return {'quotes': quotes, 'error': error}


@view_config(
    renderer='geru:templates/quote.jinja2',
    route_name='quote_rnd'
)
def quote_rnd(request):
    """
    View that shows a random quote.
    """
    data = get_quotes()
    quote = error = None
    if data['status']:
        quote = data['data']
        qid = random.choice(range(len(quote)))
        quote = quote[qid]
    else:
        error = data['error']
        qid = ''
    return {'quote': quote, 'error': error, 'qid': qid}


@view_config(
    renderer='geru:templates/quote.jinja2',
    route_name='quote'
)
def quote(request):
    """
    View that shows a specific quote.
    """
    qid = request.matchdict['qid']
    data = get_quote(qid)
    quote = error = None
    if data['status']:
        quote = data['data']
    else:
        error = data['error']
    return {'quote': quote, 'error': error, 'qid': qid}
