# -*- coding: utf-8 -*-

from django.template import RequestContext
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.conf import settings
from django.core.mail import send_mail
from gouache.pagamento_digital.models import Cliente
from django.utils.encoding import smart_str


from gouache.django_cart.cart import Cart
from gouache.loja.models import Tamanhocor, Produto



def add(request):
    '''
    View para adicionar um produto ao carrinho.
    '''

    cart = Cart(request)
    try:
        if request.method == 'POST':
            dados = request.POST
            produto = Tamanhocor.objects.get(id=dados.get('produto'))
            quantidade = int( dados.get('produto') )

            if produto.produto.promocao:
                cart.add(produto, produto.produto.preco_promocao, quantidade)
            else:
                cart.add(produto, produto.produto.preco, quantidade)

            return HttpResponse(1)
        else:
            return HttpResponse(0)
    except:
        return HttpResponse(0)



def remove(request):
    '''
    View para remover um produto do carrinho.
    '''

    cart = Cart(request)
    try:
        produto = Tamanhocor.objects.get(id=produto_id)
        cart.remove(produto)

        return HttpResponse(1)
    except:
        return HttpResponse(0)



def update(request, produto_id, quantidade=0.0, preco=0.0):
    '''
    View para remover um produto do carrinho.
    '''

    cart = Cart(request)
    try:
        produto = Tamanhocor.objects.get(id=produto_id)
        cart.update(produto, quantidade, preco)

        return HttpResponse(1)
    except:
        return HttpResponse(0)