import requests
from requests.adapters import HTTPAdapter

from geru.cache import short_cache

API = 'https://1c22eh3aj8.execute-api.us-east-1.amazonaws.com/challenge/quotes'

session = requests.Session()
session.mount(API, HTTPAdapter(max_retries=5))

TIMEOUT = 30


@short_cache.cache_on_arguments()
def request_json(url, key=None):
    '''
    Requests json data in the provided url.
    Extracts the data from the json, given the `key`.
    If the key isn't present, just ignores it.
    '''
    output = {'status': False}
    try:
        r = session.get(url=url, stream=True, timeout=TIMEOUT)
        rj = r.json()
        if 'error' in rj:
            output['error'] = rj['error']
        else:
            if key is not None:
                output['data'] = rj[key] if key in rj else rj
            else:
                output['data'] = rj
            output['status'] = True
    except Exception as e:
        # for any error, just output the error message
        output['error'] = str(e)
    return output


def get_quotes():
    """
    Queries the API and returns a python dictionary containing all quotes available.
    """
    data = request_json(url=API, key='quotes')
    return data


def get_quote(quote_number):
    """
    Queries the API and returns a python dictionary containing the corresponding quote.
    """
    data = request_json(url=f'{API}/{quote_number}', key='quote')
    return data
