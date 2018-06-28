#-*- encoding: utf-8 -*-

import codecs
from datetime import datetime
import json
import sys
import urllib2

import bottle

from sqlalchemy import (
    Column,
    create_engine,
    DateTime,
    event,
    Integer,
    String
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import (
    scoped_session,
    sessionmaker
)

default_port = '8080'
testing = False

Base = declarative_base()

if len(sys.argv) > 2:   # pragma: no cover
    default_port = sys.argv[2]
    if sys.argv[1] == 'testing':
        testing = True
if testing:
    engine = create_engine('sqlite:///:memory:', echo=False)
else:
    engine = create_engine('sqlite:///db.sqlite3', echo=True)

DBSession = scoped_session(sessionmaker(
    autoflush=False,
    expire_on_commit=True))
DBSession.bind = engine


class Person(Base):
    __tablename__ = 'person'

    facebookId = Column(String(255), primary_key=True)
    username = Column(String(255))
    name = Column(String(255))
    gender = Column(String(55))

    def __repr__(self):
        return u"<Person('%s', '%s')>" % (self.facebookId, self.name)

    def to_dict(self):
        return dict(
            [(k, self.__dict__[k]) for k in sorted(self.__dict__)
                if '_sa_' != k[:4]])


class Log(Base):
    __tablename__ = 'log'
    __table_args__ = {'sqlite_autoincrement': True}

    id = Column(Integer, primary_key=True)
    acao = Column(String(2), nullable=False)
    #V - View
    #U - Update
    #I - Insert
    #D - Delete
    corpo = Column(String(255), nullable=False)
    horario = Column(DateTime, default=datetime.now)

    def __repr__(self):
        return u"<Log (%s)>" % (self.horario)

    def to_dict(self):
        return dict(
            [(k, self.__dict__[k]) for k in sorted(self.__dict__)
                if '_sa_' != k[:4]])


@event.listens_for(Person, 'after_delete')
def person_after_delete(mapper, connection, target):
    """
    Gatilho para gerar log de objetos apagados.
    """
    trans = connection.begin()
    log = Log.__table__
    connection.execute(
        log.insert()
        .values({
            'corpo': unicode(target),
            'acao': 'D',
        })
    )
    trans.commit()


@event.listens_for(Person, 'after_insert')
def person_after_insert(mapper, connection, target):
    """
    Gatilho para gerar log de objetos inseridos.
    """
    trans = connection.begin()
    log = Log.__table__
    connection.execute(
        log.insert()
        .values({
            'corpo': unicode(target),
            'acao': 'I',
        })
    )
    trans.commit()


@event.listens_for(Person, 'after_update')
def person_after_update(mapper, connection, target):
    """
    Gatilho para gerar log de objetos atualizados.
    """
    trans = connection.begin()
    log = Log.__table__
    connection.execute(
        log.insert()
        .values({
            'corpo': unicode(target),
            'acao': 'U',
        })
    )
    trans.commit()


app = bottle.Bottle()


if testing:
    class ExternalRequests(object):
        def request(self, address):
            facebookId = address.rsplit('?', 1)[0].rsplit('/', 1)[1]
            with codecs.open('test_data.json', 'r', 'utf-8') as f:
                data = json.loads(f.read())

            try:
                contents = data[facebookId]
            except KeyError:
                raise urllib2.HTTPError(
                    address, 404, 'Error 400/404', None, None)
            contents['id'] = contents['facebookId']
            return contents
else:   # pragma: no cover
    class ExternalRequests(object):
        def request(self, address):
            req = urllib2.Request(address)
            resp = urllib2.urlopen(req)

            contents = json.loads(resp.read())
            return contents


@app.route('/')
def home():
    contents = {
        'success': True,
        'message': 'Seja bem vindo a home do projeto'}
    DBSession.add(Log(**{
        'acao': 'V',
        'corpo': u'Alguém visitou a home'}))
    DBSession.flush()
    return bottle.HTTPResponse(
        status=200, body=contents,
        headers={"Content-Type": "application/json"})


@app.route('/person/', method='POST')
def person_insert(kwargs=None):
    '''
    View que recebe o parâmetro facebookId via post, recupera
    os dados no facebook e faz upsert no banco de dados.
    '''
    if kwargs is None:   # pragma: no cover
        kwargs = dict(bottle.request.params.items())
    fid = kwargs.get('facebookId', None)

    DBSession.add(Log(**{
        'acao': 'V',
        'corpo': u'Alguém acessou a view para inserir cadastros.'}))
    DBSession.flush()

    if fid:
        try:
            address = 'https://graph.facebook.com/%s?fields=%s' % (
                fid, ','.join(['name', 'gender', 'username']))
            req = ExternalRequests()
            req.request(address)
            contents = req.request(address)
        except urllib2.HTTPError as e:
            status = e.code
            contents = {'error': unicode(e), 'created': False}
        except Exception as e:   # pragma: no cover
            status = 400
            contents = {'error': unicode(e), 'created': False}

        if 'error' not in contents:
            #se ocorreu algum erro ao tentar recuperar os dados
            #p.e. usuário/página inexistente

            faceid = contents['id']
            username = contents['username']
            name = contents['name']
            gender = contents['gender']
            if DBSession.query(Person).filter_by(facebookId=fid).count() == 0:
                p = Person(
                    facebookId=faceid,
                    username=username,
                    name=name,
                    gender=gender)
                DBSession.add(p)
                DBSession.flush()
                DBSession.commit()
                status = 201
                contents['created'] = True
            else:
                p = DBSession.query(Person).get(fid)
                p.id = faceid
                p.username = username
                p.name = name
                p.gender = gender
                DBSession.merge(p)
                DBSession.flush()
                DBSession.commit()
                status = 200
                contents['created'] = False
        return bottle.HTTPResponse(
            status=status, body=contents,
            headers={"Content-Type": "application/json"})
    else:
        contents = {'error': u'Empty facebookId.', 'created': False}
        return bottle.HTTPResponse(
            status=400, body=contents,
            headers={"Content-Type": "application/json"})


@app.route('/person/', method='GET')
def person_list(kwargs=None):
    '''
    View para listagem dos dados. Recebe os parâmetros:
    limit: número de resultados
    '''

    DBSession.add(Log(**{
        'acao': 'V',
        'corpo': u'Alguém acessou a view para listar cadastros.'}))
    DBSession.flush()

    if kwargs is None:   # pragma: no cover
        try:
            kwargs = dict(bottle.request.params.items())
        except KeyError:
            pass
    try:   # pragma: no cover
        limit = int(kwargs.get('limit', 0)) if kwargs else 0
    except ValueError:
        contents = {'error': u'Invalid limit.'}
        return bottle.HTTPResponse(
            status=400, body=json.dumps(contents),
            headers={"Content-Type": "application/json"})

    query = DBSession.query(Person)
    if limit > 0:
        query = query.limit(limit)

    people = [
        p.to_dict() for p in query]

    return bottle.HTTPResponse(
        status=200, body=json.dumps(people),
        headers={"Content-Type": "application/json"})


@app.route('/person/<fid>', method='GET')
def person_show(fid):
    '''
    View para exibir os dados de uma pessoa específica.
    '''

    DBSession.add(Log(**{
        'acao': 'V',
        'corpo': u'Alguém acessou a view para exibir ' +
                 u'dados de um cadastro específico.'}))
    DBSession.flush()

    if fid:
        try:
            if DBSession.query(Person).filter_by(facebookId=fid).count() == 0:
                return bottle.HTTPResponse(
                    status=404, body={'error': 'Not found.'})
            else:
                person = DBSession.query(Person).get(fid)
                return bottle.HTTPResponse(
                    status=200, body=person.to_dict())
        except:
            return bottle.HTTPResponse(
                status=400, body={'error': u'Invalid facebookId.'},
                headers={"Content-Type": "application/json"})
    else:
        return bottle.HTTPResponse(
            status=400, body={'error': u'No facebookId specified.'},
            headers={"Content-Type": "application/json"})


@app.route('/person/<fid>', method='DELETE')
def person_delete(fid):
    '''
    View para apagar uma pessoa.
    '''
    DBSession.add(Log(**{
        'acao': 'V',
        'corpo': u'Alguém acessou a view para apagar cadastros.'}))
    DBSession.flush()

    if fid:
        if DBSession.query(Person).filter_by(facebookId=fid).count() == 0:
            return bottle.HTTPResponse(
                status=404, body={'error': 'Not found.'},
                headers={"Content-Type": "application/json"})
        else:
            p = DBSession.query(Person).get(fid)
            DBSession.delete(p)
            DBSession.flush()
            return bottle.HTTPResponse(
                status=204,
                headers={"Content-Type": "application/json"})
    else:
        return bottle.HTTPResponse(
            status=400, body={'error': u'Invalid facebookId.'},
            headers={"Content-Type": "application/json"})


if __name__ == '__main__':   # pragma: no cover
    import os
    path = os.path.dirname(os.path.realpath(__file__))
    dbpath = os.path.join(path, 'db.sqlite3')

    try:
        DBSession.query(Person).all()
    except:
        Base.metadata.create_all(engine)
    app.run(host='localhost', port=default_port, debug=True, reloader=True)
