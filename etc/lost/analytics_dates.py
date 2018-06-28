# you can write to stdout for debugging purposes, e.g.
# print("this is a debug message")

from datetime import datetime
from operator import itemgetter
import re


DAYS = ('Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun')


def make_calendar(S):
    calendar = []

    for s in S.split('\n'):
        day, start, end = re.split('[- ]', s)
        start = list(map(lambda x: int(x), start.split(':')))
        end = list(map(lambda x: int(x), end.split(':')))
        cur_day = DAYS.index(day) + 1
        start_meet_time = datetime(2018, 1, cur_day, *start)
        if end[0] == 24:
            end[0] = 0
            cur_day += 1
        end_meet_time = datetime(2018, 1, cur_day, *end)
        calendar.append({
            'start': start_meet_time,
            'end': end_meet_time
        })

    calendar.sort(key=itemgetter('start'))
    return calendar


def solution(S):
    # write your code in Python 3.6
    calendar = make_calendar(S)

    longest_free_time = 0
    start_free_time = datetime(2018, 1, 1, 0, 0)
    for meeting in calendar:
        free_time = int((meeting['start'] - start_free_time).seconds / 60)
        start_free_time = meeting['end']

        if free_time > longest_free_time:
            longest_free_time = free_time

    # deals with the last piece of the last day
    end_free_time = datetime(2018, 1, 8, 0, 0)
    free_time = int((end_free_time - start_free_time).seconds / 60)

    if free_time > longest_free_time:
        longest_free_time = free_time
    return longest_free_time
