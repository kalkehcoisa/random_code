#-*- coding: utf-8 -*-

from pyramid.response import Response
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError

from .models import (
    DBSession,
    MyModel,
)


@view_config(
    route_name='home',
    renderer='templates/home.html')
def home(request):
    return {}


@view_config(
    route_name='produtos',
    renderer='templates/produtos.html')
def produtos(request):
    return {}


@view_config(
    route_name='contato',
    renderer='templates/contato.html')
def contato(request):
    return {}
