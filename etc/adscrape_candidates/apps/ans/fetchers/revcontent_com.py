# -*- coding:utf-8 -*-
'''
    works: True (2015-12-23),
    async: fixed (2015-12-23),
'''

import re
from bs4 import BeautifulSoup
from collections import defaultdict
from datetime import datetime
from tornado import gen
from urllib import parse as urlparse
from apps.ans.fetchers.utils.async_session import AsyncSession


class RevcontentCom(object):
    ''' This is a shorted version of one of ours fetchers that we use in
        production. Use it as a guidance on how to write your own fetchers.
    '''
    
    TITLE = 'RevContent'
    NETWORK_ID = 'revcontent.com'


    @gen.coroutine
    def fetch(self, parameters):
        # creating an async session object
        session = AsyncSession(fetch_defaults={
            'headers': {
                'Host': 'www.revcontent.com',
                'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:38.0)'
                        ' Gecko/20100101 Firefox/38.0',
                'Accept': '*/*',
                'Connection': 'keep-alive',
            }
        })

        # login
        yield session.get('https://www.revcontent.com/login')
        payload = {
            'name': parameters.get('login'),
            'password': parameters.get('password'),
            'login': 'Sign In',
        }
        r = yield session.post('https://www.revcontent.com/login', payload,
            headers={
                'Referer': 'https://www.revcontent.com/login',
            })

        if r.effective_url != 'https://www.revcontent.com/dashboard':
            raise Exception('Failed to login')

        domain = 'all'
        resolution = 'all'
    
        # getting data
        start_date = parameters.get('date-start')
        end_date = parameters.get('date-end')

        link_base = 'https://www.revcontent.com/widgets'
        qs_data = {
                'tab': 'day',
                'domain': domain,
                'resolution': resolution,
                'start_date': start_date.strftime('%Y-%m-%d'),
                'end_date': end_date.strftime('%Y-%m-%d'),
            }
        link = '%s?%s' % (link_base, urlparse.urlencode(qs_data))

        page_count = None
        page_processed = 0
        result = defaultdict(dict)
        headers = []
        last_link = link
        while page_count is None or page_processed < page_count:
            page_processed += 1
            cur_link = '%s&page=%d' % (link, page_processed)
            r = yield session.get(cur_link, headers={
                    'Referer': last_link,
                })
            last_link = cur_link

            bs_content = BeautifulSoup(r.body, 'html5lib')

            # getting page_count
            if page_count is None:
                pagination = bs_content.find('ul', {'class': 'pagination'})
                for a in pagination.findAll('a'):
                    try:
                        a_page_no = int(a.text.strip())
                    except:
                        continue
                    if page_count is None or a_page_no > page_count:
                        page_count = a_page_no
                if page_count is None:
                    raise Exception('Failed to determine page count')

            # scraping data
            table = bs_content.find('table')
            if not headers:
                for th in table.find('thead').findAll('th'):
                    text = re.sub('<[^<]+?>', ' ', str(th))
                    text = re.sub(r'\s+', ' ', text).strip()
                    headers.append(text.lower())

            for tr in table.find('tbody').findAll('tr'):
                tds = tr.findAll('td')
                for header, td in zip(headers, tds):
                    value = td.text.strip()
                    if header == 'date':
                        date = datetime.strptime(value, '%b %d, %Y')
                        date = date.strftime('%Y%m%d')
                        continue

                    result[header][date] = value

        return result
