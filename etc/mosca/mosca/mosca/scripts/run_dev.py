#-*- coding: utf-8 -*-

from mosca import app, db
from mosca.articles.models import *
from mosca.auth.models import *
import sys


def main(argv=sys.argv):
    db.init_app(app)
    with app.app_context():
        db.create_all()
        db.session.commit()
    app.run(debug=True)
