#-*- coding:utf-8 -*-

import json
import os
import signal
import socket
from subprocess import Popen, PIPE
import sys
import time
import unittest
import urllib2
import webtest

from bottle import tob
import codecs
import nose
from sqlalchemy import create_engine
from sqlalchemy import exc as sql_exc

from api import Base, DBSession, Log, Person


class ExternalRequests(object):
    def request(self, address):
        facebookId = address.rsplit('?', 1)[0].rsplit('/', 1)[1]
        with codecs.open('test_data.json', 'r', 'utf-8') as f:
            data = json.loads(f.read())

        try:
            contents = data[facebookId]
        except KeyError:
            raise urllib2.HTTPError(address, 404, 'Error 400/404', None, None)
        contents['id'] = contents['facebookId']
        return contents


class UnitTests(unittest.TestCase):
    '''
    Classe base utilizada para realizar testes
    unitários no sistema.
    '''

    def setUp(self):
        '''
        Inicializa o banco de dados.
        '''
        import api
        self.engine = create_engine('sqlite:///:memory:', echo=True)
        api.DBSession.bind = self.engine
        api.ExternalRequests = ExternalRequests

        Base.metadata.create_all(self.engine)

    def tearDown(self):
        '''
        Apaga todo o banco de dados e finaliza a sessão ao terminar de
        executar cada teste.
        '''
        import api
        Base.metadata.drop_all(self.engine)
        api.DBSession.remove()


class TestModels(UnitTests):
    '''
    Classe para os testes dos models do sistema.
    '''
    def test_person(self):
        '''
        Faz as operações básicas de CRUD com o model Person.
        '''

        #não deve ser possível criar um objeto em branco
        try:
            p = Person()
            DBSession.add(p)
            DBSession.flush()
        except sql_exc.IntegrityError:
            DBSession.rollback()
        self.assertEqual(p.facebookId, None)

        #cria um objeto completo e testa seus atributos e métodos
        p = Person(
            facebookId='131234873',
            username='jurema.carijo',
            name=u'Jurema Carijó',
            gender='female')
        DBSession.add(p)
        DBSession.flush()
        self.assertNotEqual(p, None)
        self.assertEqual(p.facebookId, '131234873')
        self.assertEqual(p.username, 'jurema.carijo')
        self.assertEqual(p.name, u'Jurema Carijó')
        self.assertEqual(p.gender, 'female')

        pes = p.to_dict()
        self.assertEqual(p.facebookId, pes['facebookId'])
        self.assertEqual(p.username, pes['username'])
        self.assertEqual(p.name, pes['name'])
        self.assertEqual(p.gender, pes['gender'])

        rep = u"<Person('%s', '%s')>" % (p.facebookId, p.name)
        self.assertEqual(unicode(p), rep)

    def test_log(self):
        '''
        Faz as operações básicas de CRUD com o model Log.
        '''

        #não deve ser possível criar um objeto em branco
        try:
            p = Log()
            DBSession.add(p)
            DBSession.flush()
        except sql_exc.IntegrityError:
            DBSession.rollback()
        self.assertEqual(p.id, None)

        #cria um objeto completo e testa seus atributos e métodos
        p = Log(
            id=8237462387,
            acao='W',
            corpo=u'Körper')
        DBSession.add(p)
        DBSession.flush()
        self.assertNotEqual(p, None)
        self.assertEqual(p.id, 8237462387)
        self.assertEqual(p.acao, 'W')
        self.assertEqual(p.corpo, u'Körper')

        log = p.to_dict()
        self.assertEqual(p.id, log['id'])
        self.assertEqual(p.acao, log['acao'])
        self.assertEqual(p.corpo, log['corpo'])
        self.assertEqual(p.horario, log['horario'])

        rep = u"<Log (%s)>" % (p.horario)
        self.assertEqual(unicode(p), rep)


def ping(server, port):
    '''
    Verifica se um servidor pode receber conexões numa porta TCP específica.
    Código obtido e adaptado de:
    https://github.com/bottlepy/bottle/blob/master/test/test_server.py
    '''
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((server, port))
        return True
    except socket.error:
        return False
    finally:
        s.close()


class UnitTestViews(UnitTests):
    '''
    Classe utilizada para realizar testes
    unitários no sistema.
    '''

    def gera_pessoas(self):
        '''
        Método auxiliar para inserir dados de pessoas
        para os testes.
        '''
        import api

        ids = [
            100001409463894, 100003025997960,
            100002677114948, 759574065, 1619357922,
            100001227665412, 100001606531815,
            100004616023613, 100003288611757]
        for i in ids:
            api.person_insert({'facebookId': i})

        ''' pragma: no cover
        Código usado somente para salvar os dados usados nos testes.
        import codecs
        contents = {
            p.facebookId: p.to_dict()
            for p in api.DBSession.query(api.Person).all()}
        with codecs.open('test_data.json', 'w', encoding='utf-8') as f:
            json.dump(
                contents, f, sort_keys=True,
                indent=4, ensure_ascii=False)'''
        return ids

    def test_home(self):
        '''
        Verifica se a home do projeto está acessível.
        '''
        import api
        r = api.home()
        self.assertEqual(r.status_code, 200)

        contents = r.body
        self.assertTrue('message' in contents)
        self.assertTrue('success' in contents)

    def test_person_insert(self):
        '''
        Testa cadastrar uma pessoa.
        '''
        import api
        r = api.person_insert({'facebookId': 'bla^bla'})
        self.assertEqual(r.status_code, 404)

        r = api.person_insert({'facebookId': None})
        self.assertEqual(r.status_code, 400)

        #testa o insert
        r = api.person_insert({'facebookId': 100000429486498})
        self.assertEqual(r.status_code, 201)
        contents = r.body
        self.assertTrue('created' in contents)
        self.assertTrue(contents['created'])

        #testa o update
        r = api.person_insert({'facebookId': 100000429486498})
        self.assertEqual(r.status_code, 200)
        contents = r.body
        self.assertTrue('created' in contents)
        self.assertFalse(contents['created'])

    def test_list(self):
        '''
        Testa a listagem de pessoas.
        '''

        import api
        r = api.person_list()
        self.assertEqual(r.status_code, 200)
        contents = json.loads(r.body)
        self.assertEqual(len(contents), 0)

        #listagem deve retornar todo mundo
        ids = self.gera_pessoas()
        r = api.person_list()
        self.assertEqual(r.status_code, 200)
        contents = json.loads(r.body)
        self.assertEqual(len(contents), len(ids))

        #listagem deve retornar somente n pessoas
        n = 3
        r = api.person_list({'limit': n})
        self.assertEqual(r.status_code, 200)
        contents = json.loads(r.body)
        self.assertEqual(len(contents), n)

        r = api.person_list({'limit': 'n'})
        self.assertEqual(r.status_code, 400)

    def test_person_show(self):
        '''
        Testa a view para ver os dados de uma pessoa.
        '''

        import api
        ids = self.gera_pessoas()
        r = api.person_show(ids[0])
        self.assertEqual(r.status_code, 200)

        r = api.person_show(1283721368)
        self.assertEqual(r.status_code, 404)

        r = api.person_show(None)
        self.assertEqual(r.status_code, 400)

        r = api.person_show(['aaaaaa'])
        self.assertEqual(r.status_code, 400)

    def test_delete(self):
        '''
        Testa a remoção de pessoas.
        '''
        import api
        ids = self.gera_pessoas()

        #apaga a pessoa
        r = api.person_delete(ids[0])
        self.assertEqual(r.status_code, 204)

        #confere se a pessoa foi apagada mesmo
        r = api.person_delete(ids[0])
        self.assertEqual(r.status_code, 404)

        r = api.person_delete(None)
        self.assertEqual(r.status_code, 400)


class FunctionalTests(unittest.TestCase):
    '''
    Classe base para os testes funcionais das views do sistema.
    '''

    server = None
    skip = None
    p = None
    port = None

    @property
    def base_url(self):
        return 'http://localhost:%s/' % self.port

    def warn(self, msg):
        sys.stderr.write('WARNING: %s\n' % msg.strip())   # pragma: no cover

    def gera_pessoas(self):
        '''
        Método auxiliar para inserir dados de pessoas
        para os testes.
        '''

        url = '/person/'
        api = webtest.TestApp(self.base_url)
        ids = [
            100001409463894, 100003025997960,
            100002677114948, 759574065, 1619357922,
            100001227665412, 100001606531815,
            100004616023613, 100003288611757]
        for i in ids:
            api.post(url, {'facebookId': i})
        return ids

    def setUp(cls):
        '''
        Inicia um servidor bottle para fazer os testes.
        Código obtido e adaptado de:
        https://github.com/bottlepy/bottle/blob/master/test/test_server.py
        '''
        cls.server = os.path.join(os.path.dirname(__file__), 'api.py')
        # Procura por uma porta livre (e um saquinho de alfafa)
        for port in range(8800, 8900):
            cls.port = port

            # Inicia o servidor de testes num subprocesso
            cmd = [sys.executable, cls.server, 'testing', str(cls.port)]
            cmd += sys.argv[1:]  # repassa os argumentos para o subprocesso

            cls.p = Popen(cmd, stdout=PIPE, stderr=PIPE)
            # Espera o socket poder receber conexões
            for i in range(100):
                time.sleep(0.1)

                # Aceita conexões?
                if ping('localhost', cls.port):
                    return

                # Servidor parou (vai se saber porquê)
                if not cls.p.poll() is None:   # pragma: no cover
                    break
            rv = cls.p.poll()   # pragma: no cover
            if rv is None:   # pragma: no cover
                raise AssertionError(
                    "O servidor demorou demais para iniciar.")
            if rv is 128:   # pragma: no cover
                # Import error
                cls.warn(
                    "Ignorando o teste do servidor %r (ImportError)."
                    % cls.server)
                cls.skip = True
                return
            if rv is 3:   # pragma: no cover
            # Porta em uso
                continue
            raise AssertionError(
                "Servidor parou com o código de erro: %d" % rv)   # pragma: no cover
        raise AssertionError(
            "Não foi possível achar uma porta livre para o servidor de testes.")   # pragma: no cover

    def tearDown(cls):
        '''
        Finaliza o servidor bottle para fazer os testes.
        Código obtido e adaptado de:
        https://github.com/bottlepy/bottle/blob/master/test/test_server.py
        '''
        if cls.skip:
            return   # pragma: no cover

        if cls.p.poll() is None:
            os.kill(cls.p.pid, signal.SIGINT)
            time.sleep(0.5)
        while cls.p.poll() is None:   # pragma: no cover
            os.kill(cls.p.pid, signal.SIGTERM)
            time.sleep(1)

        for stream in (cls.p.stdout, cls.p.stderr):   # pragma: no cover
            for line in stream:
                if tob('warning') in line.lower():
                    cls.warn(line.strip().decode('utf8'))
                elif tob('error') in line.lower():
                    raise AssertionError(line.strip().decode('utf8'))

    def test_home(self):
        '''
        Verifica se a home do projeto está acessível.
        '''
        api = webtest.TestApp(self.base_url)
        r = api.get('/')
        self.assertEqual(r.status_int, 200)

        self.assertTrue('message' in r)
        self.assertTrue('success' in r)

    def test_person_insert(self):
        '''
        Testa cadastrar uma pessoa.
        '''
        url = '/person/'
        api = webtest.TestApp(self.base_url)
        try:
            error = ''
            r = api.post(url, {'facebookId': 'bla^bla'})
        except webtest.AppError as e:
            error = e.message
        self.assertTrue(error.find('404') > -1)

        try:
            error = ''
            r = api.post(url, {'facebookId': 'bla/bla'})
        except webtest.AppError as e:
            error = e.message
        self.assertTrue(error.find('400') > -1)

        #testa o insert
        r = api.post(url, {'facebookId': 100000429486498})
        self.assertEqual(r.status_int, 201)
        contents = r.json
        self.assertTrue('created' in contents)
        self.assertTrue(contents['created'])

        #testa o update
        r = api.post(url, {'facebookId': 100000429486498})
        self.assertEqual(r.status_int, 200)
        contents = r.json
        self.assertTrue('created' in contents)
        self.assertFalse(contents['created'])

    def test_list(self):
        '''
        Testa a listagem de pessoas.
        '''

        url = '/person/'
        api = webtest.TestApp(self.base_url)
        r = api.get(url)
        self.assertEqual(r.status_int, 200)
        contents = r.json
        self.assertEqual(len(contents), 0)

        ids = self.gera_pessoas()

        #listagem deve retornar todo mundo
        r = api.get(url)
        self.assertEqual(r.status_int, 200)
        contents = r.json
        self.assertEqual(len(contents), len(ids))

        #listagem deve retornar somente n pessoas
        n = 3
        r = api.get(url, params={'limit': n})
        self.assertEqual(r.status_int, 200)
        contents = r.json
        self.assertEqual(len(contents), n)

    def test_delete(self):
        '''
        Testa a remoção de pessoas.
        '''
        url = '/person/'
        api = webtest.TestApp(self.base_url)
        ids = self.gera_pessoas()

        #apaga a pessoa
        r = api.delete(url + unicode(ids[0]))
        self.assertEqual(r.status_int, 204)

        #confere se a pessoa foi apagada mesmo
        try:
            error = ''
            r = api.get(url + unicode(ids[0]))
        except webtest.AppError as e:
            error = e.message
        self.assertTrue(error.find('404') > -1)

if __name__ == '__main__':   # pragma: no cover
    nose.main()
