''' This module collects all the fetcher constructors and creates network
    records in the database if needed.
'''

import inspect
from ... import fetchers


# this section loads all the CPM fetches constructors(classes) into the
# CPM_FETCHER_CONSTRUCTORS dictionary. All the fetches should be listed in 
# the cpm/fetchers/__init__.py file (see the file for more comments).
FETCHER_CONSTRUCTORS = {}
for _name, obj in inspect.getmembers(fetchers):
    if inspect.isclass(obj):
        if hasattr(obj, 'NETWORK_ID'):
            FETCHER_CONSTRUCTORS[obj.NETWORK_ID] = obj
