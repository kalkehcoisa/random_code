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


class CriteoCom(object):
    ''' This is a shorted version of one of ours fetchers that we use in
        production. Use it as a guidance on how to write your own fetchers.
    '''

    TITLE = 'PublishersCriteo'
    NETWORK_ID = 'publishers.criteo.com'

    def _get_validation(self, response):
        '''
        Retrieves the form validation data like csrf tokens.
        '''
        payload = {
            '__VIEWSTATE': '',
            '__VIEWSTATEGENERATOR': '',
            '__EVENTVALIDATION': '',
            '__LASTFOCUS': '',
            '__EVENTARGUMENT': '',
        }
        bs_content = BeautifulSoup(response.body, 'html5lib')

        for key in payload.keys():
            elem = bs_content.find('input', {'id': key})
            if elem is not None:
                payload[key] = elem['value']

        return payload

    def _make_aspnet_payload(
            self, response, start_date, end_date, page_number=1):
        '''
        Prepare the parameters to the next post to asp.net to make
        it believe it's a browser ahn... browsing.
        Made to also accept pagination.
        '''

        payload = self._get_validation(response=response)
        monster_key = u'ctl00$ctl00$ctl00$MainContent' +\
            u'$PublisherContent$PageContent$ctlStatsMgr$'

        payload.update({
            u'__ASYNCPOST': True,
            u'ctl00$ctl00$ctl00$ddlHeaderPrefCurrency': 2,
            monster_key + u'ddlSites': 0,
            monster_key + u'ddlZones': 0,
            monster_key + u'ddlPeriods': 9,
            monster_key + u'tbBeginDate': start_date.strftime('%m-%d-%Y'),
            monster_key + u'tbEndDate': end_date.strftime('%m-%d-%Y'),
            monster_key + u'ddlViews': 0,
            u'': u'',
        })

        if page_number == 1:
            payload.update({
                u'ctl00$ctl00$ctl00$ScriptManager1':
                    u'ctl00$ctl00$ctl00$MainContent$PublisherContent' +
                    u'$PageContent$ctlStatsMgr$UpdatePanel1' +
                    u'|ctl00$ctl00$ctl00$MainContent$PublisherContent' +
                    u'$PageContent$ctlStatsMgr$ctlExecute',
                u'__EVENTTARGET':
                    u'ctl00$ctl00$ctl00$MainContent$PublisherContent' +
                    u'$PageContent$ctlStatsMgr$ctlExecute',
            })
        else:
            payload.update({
                u'ctl00$ctl00$ctl00$ScriptManager1':
                    u'ctl00$ctl00$ctl00$MainContent$PublisherContent' +
                    u'$PageContent$ctlStatsMgr$updGrid|ctl00$ctl00$ctl00' +
                    '$MainContent$PublisherContent$PageContent' +
                    '$ctlStatsMgr$lnkPage' + str(page_number),
                'ctl00$ctl00$ctl00$MainContent$PublisherContent' +
                '$PageContent$ctlStatsMgr$ddlPagingOptions': '7',
                u'__EVENTTARGET':
                    u'ctl00$ctl00$ctl00$MainContent$PublisherContent' +
                    u'$PageContent$ctlStatsMgr$lnkPage' + str(page_number),
            })
        return payload

    @gen.coroutine
    def fetch(self, parameters):
        query_link = 'https://publishers.criteo.com/publisher/statistics/default.aspx'

        # creating an async session object
        session = AsyncSession(fetch_defaults={
            'headers': {
                'Host': 'publishers.criteo.com',
                'User-Agent':
                    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:38.0)'
                    ' Gecko/20100101 Firefox/38.0',
            }
        })

        # login
        r = yield session.get('https://publishers.criteo.com/')
        payload = self._get_validation(response=r)
        # keys to login
        payload.update({
            '__EVENTTARGET':
                'ctl00$MainContent$ctlLogin$ctlLogin$LoginBtn',
            'ctl00$MainContent$ctlLogin$ctlLogin$UserName':
                parameters.get('login'),
            'ctl00$MainContent$ctlLogin$ctlLogin$Password':
                parameters.get('password'),
        })
        r = yield session.post(
            'https://publishers.criteo.com', payload,
            headers={
                'Referer': 'https://publishers.criteo.com/',
            }
        )
        if r.effective_url != 'https://publishers.criteo.com/publisher/':
            raise Exception('Failed to login')

        # getting data
        start_date = parameters.get('date-start')
        end_date = parameters.get('date-end')

        # first access to the page to retrieve the wanted data
        # and get the first state
        r = yield session.get(
            query_link,
            headers={
                'Referer': 'https://publishers.criteo.com/publisher/',
            }
        )
        payload = self._make_aspnet_payload(r, start_date, end_date)
        r = yield session.post(
            query_link,
            data=payload,
            headers={
                'Referer': query_link,
                "X-MicrosoftAjax": "Delta = true",
                "X-Requested-With": "XMLHttpRequest",
            }
        )

        # increase the pages size to show everything' at once
        payload = self._make_aspnet_payload(r, start_date, end_date)
        payload.update({
            u'ctl00$ctl00$ctl00$ScriptManager1':
                u'ctl00$ctl00$ctl00$MainContent$PublisherContent$PageContent' +
                u'$ctlStatsMgr$updGrid|ctl00$ctl00$ctl00$MainContent' +
                u'$PublisherContent$PageContent$ctlStatsMgr$ddlPagingOptions',
            u'ctl00$ctl00$ctl00$MainContent$PublisherContent' +
            u'$PageContent$ctlStatsMgr$ddlPagingOptions': '0',
            u'__EVENTTARGET':
                u'ctl00$ctl00$ctl00$MainContent$PublisherContent' +
                u'$PageContent$ctlStatsMgr$ddlPagingOptions',
        })
        r = yield session.post(
            query_link,
            data=payload,
            headers={
                'Referer': query_link,
                "X-MicrosoftAjax": "Delta = true",
                "X-Requested-With": "XMLHttpRequest",
            }
        )
        bs_content = BeautifulSoup(r.body, 'html5lib')
        table_block = bs_content.find(
            'div',
            {
                'id': u'ctl00_ctl00_ctl00_MainContent_Publisher' +
                'Content_PageContent_ctlStatsMgr_updGrid'
            }
        )

        if table_block is None:
            # sometimes their server stop answering
            # and give a message with a code to provide
            # to their suport
            error = bs_content.find(
                'div', {'id': 'ctl00_InformationControl1_p'}
            ).findAll('li')
            raise Exception('\n'.join(str(msg.text) for msg in error))

        result = defaultdict(dict)
        table = table_block.find('table', {'class': 'BoundGrid'})

        # in case there is no data
        if 'No data to display' in table.text:
            return result

        # scrape the data table
        for tr in table.find('tbody').findAll('tr'):
            row = tr.findAll('td')
            day = datetime.strptime(
                row[0].text.split(' ')[1],
                '%d/%m/%Y').strftime('%Y%m%d')

            result['impressions'][day] = row[1].text
            result['ctr'][day] = row[4].text.split(' ')[0]
            result['cpm'][day] = row[5].text.split(' ')[0]
            result['revenue'][day] = row[6].text

        return result
