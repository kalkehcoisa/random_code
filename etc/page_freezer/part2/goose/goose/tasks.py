from collections import Counter, deque, namedtuple
from datetime import datetime
import time

from huey import crontab
import requests
from requests.adapters import ConnectionError, HTTPAdapter
from requests.exceptions import HTTPError, Timeout
from requests.models import MissingSchema
from sortedcontainers import SortedList

from config import hueymq
from logs import logger


session = requests.Session()
session.mount('about:blank', HTTPAdapter(max_retries=5))


WaitData = namedtuple('WaitData', ('url', 'start', 'wait'))


class Statistics(object):
    """
    To grant the values aren't going to be reset/recreated.

    (TODO) The system was reseting them, haven't figured out
    how or why.
    """
    _singleton = None
    data = {
        'urls_checked': 0,
        'current_urls': deque(),
        'http_codes': Counter(),
        'longest_waits': SortedList(key=lambda x: x.wait),
        'waits': deque()
    }

    def __new__(cls, *args, **kwargs):
        if cls._singleton is None:
            cls._singleton = object.__new__(Statistics)
        return cls._singleton

    @classmethod
    def remove_old_tasks(cls):
        """
        Adds the longest lasting url check to the main list
        while clearing the list.
        """
        if len(cls.data['waits']) > 0:
            wd = cls.data['waits'][0]
            while len(cls.data['waits']) > 0:
                item = cls.data['waits'].popleft()
                if item.wait >= wd.wait:
                    wd = item
            cls.data['longest_waits'].add(wd)

    @classmethod
    def remove_oldests(cls):
        """
        Remove all the old tasks (older than 5 minutes)
        """
        ref = time.time()
        for i, t in enumerate(cls.data['longest_waits']):
            if ref - t.start >= 300.0:
                print(t)
                cls.data['longest_waits'].pop(i)


STATS = Statistics()


@hueymq.periodic_task(crontab(minute='*'))
@hueymq.lock_task('add_to_oldest_waits')
def add_to_oldest_waits():
    """
    Process the waiting time data from STATS.data['waits']
    to the STATS.data['longest_waits'].
    Gets the longest wait item from the first list
    to the second one while clearing the first.
    Also, clears the oldest run times
    from the STATS.data['longest_waits']

    The first list is a deque: safe to append/pop async.
    """

    STATS.remove_oldests()
    STATS.remove_old_tasks()

    # calls the logging manually to grant running order
    do_the_logging()


def do_the_logging(logger=logger):
    """
    Prints the required log into a file called logs.log every minute.
        - how many URLs have been checked so far;
        - what URLS are currently being checked;
        - top 5 HTTP codes returned across all urls;
        - URL that took the longest to check in the past 5 minutes;
    """
    logger.info('Checked URLS: {}'.format(STATS.data['urls_checked']))
    logger.info('Top 5 HTTP statuses: {}'.format(', '.join(
        '%s: %s' % (h, n)
        for h, n in STATS.data['http_codes'].most_common(5)
    )))
    longest = max(
        (i for i in STATS.data['longest_waits']),
        key=lambda k: k.wait
    )
    logger.info('Longest check time: {} - URL {}'.format(
        longest.wait, longest.url
    ))


def inner_increase_counter(retval):
    STATS.data['urls_checked'] += 1
    status = retval.get('status_code')
    STATS.data['http_codes'].update([status])


@hueymq.task(retries=50, retry_delay=1)
@hueymq.lock_task('increase_counter')
def increase_counter(retval):
    """
    Just increase the number counter of checked urls
    and also adds the http status to the counter.
    """
    inner_increase_counter(retval)


@hueymq.task(retries=50, retry_delay=1)
@hueymq.lock_task('add_wait')
def add_wait(url, start, wait):
    """
    Just adds a check to the list of waiting times.
    """
    STATS.data['waits'].append(WaitData(url, start, wait))


def gather_stats(func):
    """
    This decorator gathers data about every request to an url:
     - url, response time, http status
    """
    def wrapper(url, interval):
        STATS.data['current_urls'].append(url)
        start = time.time()
        retval = func(url, interval)
        end = time.time()
        STATS.data['current_urls'].remove(url)

        increase_counter.schedule(args=(retval, ))
        add_wait.schedule(args=(url, start, (end - start)))

        print('{start} - {url} - {size} Bytes'.format(
            start=datetime.fromtimestamp(start).strftime('%d/%m/%Y %H:%M:%S'),
            url=url,
            size=retval['size'])
        )
        return retval
    return wrapper


def get_size(response):
    """
    Get the content size of a response (if defined).
    """
    if response is None:
        return None
    return sum(len(chunk) for chunk in response.iter_content(8196)) or 0


@hueymq.task()
@gather_stats
def periodic_check_url(url, interval):
    """
    This task check an url `url` in intervals of `interval`.
    It reschedule itself every run to act periodicaly. Since, huey periodic_task
    works minimum with one minute.

    This method handles exceptions and logs the ones that it is unable to handle.
    Keeps trying to recheck every url.

    - In case of `Timeout`, waits twice the time before the next check.
    - For `ConnectionError` or `HTTPError`, it doubles the check interval
    permanentely to reduce the number of errors, but doesn't stop
    tracking the url.
    - Only in case of `MissingSchema` (invalid url) that the system stops tracking.
    Since it's invalid, there is no point on checking again.
    An approach could be try to correct the url with some variants, but I thought
    better to stick to the main task.
    """

    # recall this task to make it run as a periodic one
    # (huey limitation: minimum precision of minutes for periodical tasks)
    res = periodic_check_url.schedule(args=(url, interval), delay=interval)
    check_stats = {
        'size': None,
        'status_code': None,
        'error': None
    }

    kw = {'url': url, 'stream': True, 'timeout': max(interval / 10, 20)}
    try:
        response = session.get(**kw)
        check_stats['size'] = get_size(response)
        check_stats['status_code'] = response.status_code
    except (ConnectionError, HTTPError) as e:
        # e.g. DNS failure, refused connection, etc
        # invalid HTTP response
        # doubles the waiting to recheck this url
        res.revoke()
        periodic_check_url.schedule(
            args=(url, interval * 2), delay=(interval * 2)
        )
        check_stats['error'] = e
        check_stats['size'] = get_size(e.response)
        if isinstance(e, HTTPError):
            check_stats['status_code'] = e.response.status_code
        return check_stats
    except Timeout as e:
        # timeout: adds some more waiting, but doesn't increase the waiting
        # in the chain of calls
        res.revoke()
        check_stats['error'] = e
        check_stats['size'] = get_size(e.response)
        periodic_check_url.schedule(
            args=(url, interval), delay=(interval * 2)
        )
        return check_stats
    except MissingSchema as e:
        # invalid url: don't ever retry it
        check_stats['error'] = e
        res.revoke()
        return check_stats
    except Exception as e:
        # unexpected error
        check_stats['error'] = e
        logger.error(str(e))

    return check_stats
