#!/usr/bin/env python3

import re
import time

from bs4 import BeautifulSoup
import requests

from mailer import send_mail
from database import TinyDBManager


class Packtpub(object):
    '''
    Crawler para a Packtpub.
    '''

    __config = {
        'url.base': 'https://www.packtpub.com',
        'url.login': '/packt/offers/free-learning',
        'url.download': '/ebook_download/{0}/{1}',

        'login.email': '',
        'login.password': '',

        'email.to_mail': '',

        'debug': False,
    }
    info = {
        'paths': []
    }
    __delay = 5

    def __init__(self):
        self.url_base = self.__config.get('url.base')
        self.__headers = self.gen_headers()
        self.__session = requests.Session()

    def gen_headers(self):
        # improvement: random user agent
        return {
            'Accept': 'text/html,application/xhtml+xml,\
            application/xml;q=0.9,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 \
            (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'
        }

    def make_soup(self, response):
        return BeautifulSoup(response.text, 'html5lib')

    def _get_login_data(self):
        url = self.url_base
        url += self.__config['url.login']

        response = self.__session.get(url, headers=self.__headers)

        soup = self.make_soup(response)
        form = soup.find('form', {'id': 'packt-user-login-form'})
        self.info['form_build_id'] = form.find('input', attrs={
            'name': 'form_build_id'})['value']
        self.info['form_id'] = form.find(
            'input', attrs={'name': 'form_id'})['value']

    def _login(self):
        data = self.info.copy()
        data['email'] = self.__config.get('login.email')
        data['password'] = self.__config.get('login.password')
        data['op'] = 'Login'
        # print '[-] data: {0}'.format(urllib.urlencode(data))

        url = self.url_base
        response = None
        url += self.__config.get('url.login')
        response = self.__session.post(url, headers=self.__headers, data=data)

        soup = self.make_soup(response)
        div_target = soup.find('div', {'id': 'deal-of-the-day'})

        title = div_target.select('div.dotd-title > h2')[0].text.strip()
        self.info['title'] = title
        self.info['filename'] = ''.join(
            [i if ord(i) < 128 else ' ' for i in title]).replace('', '_')
        self.info['description'] = div_target.select(
            'div.dotd-main-book-summary > div')[2].text.strip()

        urls = div_target.select('div.dotd-main-book-image img')
        url_image = list(filter(lambda x: 'data-original' in x.attrs, urls))[0]

        self.info['url_image'] = 'https:' + url_image['data-original']
        self.info['url_claim'] = self.url_base + div_target.select(
            'a.twelve-days-claim')[0]['href']
        # remove useless info
        self.info.pop('form_build_id', None)
        self.info.pop('form_id', None)

    def _get_claim(self):
        '''
        Pega o livro do dia.
        '''
        url = self.info['url_claim']

        response = self.__session.get(url, headers=self.__headers)

        soup = self.make_soup(response)
        div_target = soup.find('div', {'id': 'product-account-list'})

        # only last one just claimed
        div_claimed_book = div_target.select('.product-line')[0]
        self.info['book_id'] = div_claimed_book['nid']
        self.info['author'] = div_claimed_book.find(
            class_='author').text.strip()

        source_code = div_claimed_book.find(
            href=re.compile('/code_download/*'))
        if source_code is not None:
            self.info['url_source_code'] = self.url_base + source_code['href']

        # if stores a new ebook, then send it by email, message, etc
        if self._store():
            self._log()

    def _log(self):
        to_mail = self.__config['email.to_mail']

        title = 'Ebook: "{title}"'.format(
            title=self.info['title']
        )
        message = '''
            <br/><img src="{src}" /><br/>
            <p>{filename}<br/>{description}</p><br/>
            <p><a href="{url_claim}">URL to Claim</a></p>
        '''.format(
            src=self.info['url_image'],
            description=self.info['description'],
            filename=self.info['filename'],
            url_claim=self.info['url_claim'],
        )

        send_mail(message, title, to_mail)

    def _store(self):
        '''
        Checks if the ebook has already been claimed in the database.
        If not, save to the database, email the user, etc.
        Returns True if it's a new record in the database.
        '''

        db = TinyDBManager()
        check = db.check('book_id', self.info['book_id'])
        if check:
            db.insert(self.info)

        return check

    def run(self):
        """
        """

        self._get_login_data()
        time.sleep(self.__delay)
        self._login()
        time.sleep(self.__delay)
        self._get_claim()
        time.sleep(self.__delay)


if __name__ == '__main__':
    crawler = Packtpub()
    crawler.run()


class PackpubOld(object):
    """
    """

    def download_ebooks(self, types):
        """
        """

        downloads_info = [dict(
            type=type,
            url=self.url_base + self.__config.get(
                'url', 'url.download').format(self.info['book_id'], type),
            filename=self.info['filename'] + '.' + type)
            for type in types]

        directory = self.__config.get('path', 'path.ebooks')
        for download in downloads_info:
            self.info['paths'].append(download_file(
                self.__session, download['url'], directory,
                download['filename'], self.__headers))

    def download_extras(self):
        """
        """

        directory = self.__config.get('path', 'path.extras')

        url_image = self.info['url_image']
        filename = self.info['filename'] + '_' + split(url_image)[1]
        self.info['paths'].append(download_file(
            self.__session, url_image, directory, filename, self.__headers))

        if 'url_source_code' in self.info:
            self.info['paths'].append(download_file(
                self.__session, self.info['url_source_code'], directory,
                self.info['filename'] + '.zip', self.__headers))
