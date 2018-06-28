#-*- coding: utf-8 -*-

from mosca import app, db
from mosca.admin.models import *
from mosca.articles.models import *
import sys
from werkzeug.security import generate_password_hash


def main(argv=sys.argv):
    db.init_app(app)
    with app.app_context():
        db.drop_all()
        db.create_all()

        items = [
            {'title': 'Frameworks',
             'order': 0},
            {'title': 'Bancos de dados/ORMs',
             'order': 1},
            {'title': 'Ferramentas',
             'order': 2},
            {'title': 'Testes',
             'order': 3},
            {'title': 'Versionamento',
             'order': 4},
            {'title': 'Mais',
             'order': 99999}]
        for cat in items:
            db.session.add(Category(**cat))
        db.session.commit()

        pframe = Category.query.filter_by(title='Frameworks').first()
        frameworks = [
            {'title': 'Bottle', 'parent': pframe.id, 'order': 0},
            {'title': 'Django', 'parent': pframe.id, 'order': 0},
            {'title': 'Flask', 'parent': pframe.id, 'order': 0},
            {'title': 'Pyramid', 'parent': pframe.id, 'order': 0},
            {'title': 'Web2py', 'parent': pframe.id, 'order': 0}]
        for frame in frameworks:
            db.session.add(Category(**frame))
        db.session.commit()

        test_user = User(
            username="test",
            email="test@test.com.br",
            password=generate_password_hash("test"))
        db.session.add(test_user)
        db.session.commit()
