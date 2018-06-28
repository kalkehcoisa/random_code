from collections import defaultdict
from datetime import timedelta
from tornado import gen



class ExampleFetcherCom(object):
    ''' This is an example fetcher that does not return real data. It's just for
    demonstration of what kind of data "fetch" method should return.
    '''
    
    TITLE = 'Example Fetcher'
    NETWORK_ID = 'example-fetcher.com'
    
    METRICS = ['cpm', 'revenue', 'impressions']
    
    
    @gen.coroutine
    def fetch(self, parameters):
        ''' This method should return data scraped from a network.
        The "parameters" argument is a dictionary that contains this data:
            date-start - a datetime object representing starting date for the
                report.
            date-end - a datetime object for end date.
            login - login to use with the network.
            password - password to use.
        
        This method should return data(dictionary) in this format:
            {
                __metric__: {
                    __date__: __value___,
                    ...
                },
                ...
            }
            
        Where:
            __metric__ - whatever metric you want to return, most common once
                are 'cpm', 'impressions' and 'revenue'.
            __date__ - a date string in format "%Y%m%d" (no dashes).
            __value__ - metric's value for the date.
            
        This method should be an asynchronous one, so you cannot use a request
        library, use apps.ans.fetchers.utils.async_session.AsyncSession
        object instead. Example:
        
        # somewhere at the top
        from  apps.ans.fetchers.utils.async_session import AsyncSession
        
        # then in your fetch method:
        session = AsyncSession(fetch_defaults={
            'headers': {
                'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:38.0)'
                        ' Gecko/20100101 Firefox/38.0',
                'Accept': '*/*',
                'Connection': 'keep-alive',
            }
        })
        # make an async request and wait for a result
        r = yield session.get('http://some-url.com', headers={
            'Some-Header': 'header value',
        })
        # print out the response text
        print(r.body.decode()) # body is a sequence of bytes
        '''
        
        date_current = parameters.get('date-start')
        date_end = parameters.get('date-end')
        one_day = timedelta(days=1)
        
        result = defaultdict(dict)
        number = 1
        while date_current <= date_end:
            date_str = date_current.strftime('%Y%m%d')
            
            result['cpm'][date_str] = 2
            result['impressions'][date_str] = number * 1000
            result['revenue'][date_str] = (
                (result['cpm'][date_str] / 1000) *
                    result['impressions'][date_str])
            
            number += 1
            date_current += one_day
        
        
        return result