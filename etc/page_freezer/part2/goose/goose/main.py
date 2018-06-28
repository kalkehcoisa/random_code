import json
import os

from config import hueymq  # noqa
from tasks import periodic_check_url


PATH = os.path.dirname(os.path.realpath(__file__))
urls = json.load(open(
    os.path.join(PATH, 'urls2.json')
))

if __name__ == '__main__':
    for item in urls:
        print('Adding url {url} with interval {interval}'.format(**item))
        periodic_check_url(**item)
