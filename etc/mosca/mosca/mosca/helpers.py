#-*- coding: utf-8 -*-


import unicodedata
from unidecode import unidecode
import re

_punct_re = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.]+')


def permalinkify(text, delim=u'-'):
    """Generates an ASCII-only permalink."""
    result = []
    for word in _punct_re.split(text.lower()):
        result.extend(unidecode(word).split())
    return str(delim.join(result))


def strip_accents(s):
    return u''.join(
        c for c in unicodedata.normalize('NFD', s)
        if unicodedata.category(c) != 'Mn')
