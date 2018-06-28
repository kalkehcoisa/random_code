from collections import Counter, deque
import time

import pytest


def clear_statistics():
    """
    Helper for testing: since it's a singleton,
    the data has to be hard cleaned.
    """
    from sortedcontainers import SortedList
    import tasks
    stats = tasks.Statistics()
    stats.__class__.data = {
        'urls_checked': 0,
        'current_urls': deque(),
        'http_codes': Counter(),
        'longest_waits': SortedList(key=lambda x: x.wait),
        'waits': deque()
    }


@pytest.mark.unit
def test_statistics():
    import tasks

    stats = tasks.Statistics()
    stats2 = tasks.Statistics()

    # check if it's properly working as a singleton
    assert id(stats) == id(stats2)
    assert 'urls_checked' in stats.data
    clear_statistics()


@pytest.mark.unit
def test_statistics_remove_old_tasks():
    from tasks import Statistics, WaitData

    stats = Statistics()
    assert len(stats.data['waits']) == 0
    assert len(stats.data['longest_waits']) == 0

    wait = WaitData('', 1, 2)
    # add a wait
    stats.data['waits'].append(wait)
    assert len(stats.data['waits']) == 1
    assert len(stats.data['longest_waits']) == 0

    # move a wait
    stats.remove_old_tasks()
    assert len(stats.data['waits']) == 0
    assert stats.data['longest_waits'][0] == wait
    clear_statistics()


@pytest.mark.unit
def test_statistics_remove_oldests():
    from tasks import Statistics, WaitData

    stats = Statistics()
    assert len(stats.data['longest_waits']) == 0
    stats.data['longest_waits'].add(WaitData('', (time.time() - 225), 10))
    stats.data['longest_waits'].add(WaitData('', (time.time() - 350), 20))

    stats.remove_oldests()
    assert stats.data['longest_waits'][0].wait == 10
    assert len(stats.data['longest_waits']) == 1

    clear_statistics()


@pytest.mark.unit
def test_do_the_logging():
    from tasks import do_the_logging
    from tasks import Statistics, WaitData

    class Temp(object):
        msgs = []

        def info(self, msg):
            self.msgs.append(msg)

    stats = Statistics()
    wait = WaitData('', 225, 10)
    stats.data['waits'].append(wait)
    stats.data['longest_waits'].add(wait)

    logger = Temp()
    do_the_logging(logger)

    answers = [
        'Checked URLS: 0',
        'Top 5 HTTP statuses: ',
        'Longest check time: 10 - URL '
    ]
    for msg, answer in zip(logger.msgs, answers):
        assert msg == answer

    clear_statistics()


@pytest.mark.unit
@pytest.mark.parametrize('code', [
    1, 2, 3, 4, 5
])
def test_increase_counter(code):
    from tasks import inner_increase_counter, Statistics
    clear_statistics()

    stats = Statistics()
    inner_increase_counter({'status_code': code})
    assert stats.data['urls_checked'] == 1
    assert code in stats.data['http_codes']

    clear_statistics()
