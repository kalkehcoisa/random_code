#!/bin/python3


def word_count(filename):
    '''
    Reads a file based on `filename` and returns a dictionary
    with a word count.
    '''
    file = open(filename, 'r+')

    counting = {}
    for word in file.read().split():
        counting[word] = counting.get(word, 0) + 1
    return counting
