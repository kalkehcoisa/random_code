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
from gouache.loja.models import Tamanhocor, Produto, Tamanho




def cart_list(request):#, sexo='T', categoria='Todas', tamanho=0, pagina=1):
    '''
    View para listagem dos produtos no carrinho.
    '''
    cart = Cart( request )
    produto = Tamanhocor.objects.all()[0]
    quantidade = 2
    try:
        cart.add(produto, produto.produto.preco, quantidade)
    except:
        pass
    

    if request.method == 'POST':
        dados = request.POST

        num_prod = int( dados.get('num_produtos') )
        acao = dados.get('action')

        for i in range(1, num_prod+1):
            id = dados.get('tamanhocor_id_'+str(i))
            tam = dados.get('tam_'+str(i))
            quant = dados.get('quant_'+str(i))

            prod = Tamanhocor.objects.get( pk = id )
            produto = Tamanhocor.objects.get( produto = prod.produto, tamanho__tamanho = tam )

            cart.remove( prod )
            cart.add( produto, produto.produto.preco, quant )


    cart_option = 'list'
    return render_to_response('django_cart/list.html', locals(), context_instance=RequestContext(request))


def cart_add(request, produto_id, quantidade):
    '''
    View para adicionar um produto ao carrinho.
    '''
    cart = Cart(request)

    produto = Tamanhocor.objects.get(id=produto_id)
    if produto.produto.promocao:
        cart.add(produto, produto.produto.preco_promocao, quantidade)
    else:
        cart.add(produto, produto.produto.preco, quantidade)


    cart_option = 'list'
    return render_to_response('django_cart/list.html', locals(), context_instance=RequestContext(request))


def cart_remove(request, produto_id):
    '''
    View para remover um produto do carrinho.
    '''
    produto = Tamanhocor.objects.get(id=produto_id)
    cart = Cart(request)
    cart.remove(produto)


    cart_option = 'list'
    return render_to_response('django_cart/list.html', locals(), context_instance=RequestContext(request))