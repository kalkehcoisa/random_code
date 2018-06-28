#-*- coding: utf-8 -*-

from django.template import RequestContext
from django.shortcuts import render_to_response
from django.utils.encoding import smart_str



def visao_geral(request):
    '''
    '''
    
    return render_to_response('mapa/visao_geral.html', locals(), context_instance=RequestContext(request))



def viajar(request, linha, coluna):
    '''
    '''
    from mapa.functions import get_area, prepopulate_map
    from mapa.models import Terreno
    from tecnocracia import settings
    from django.core.urlresolvers import reverse
    from django.http import HttpResponseRedirect
    #from django.http import HttpResponse
    prepopulate_map()


    #neste bloco e feita a verificacao das coordenadas na navegacao
    #se extrapolar algum limite, o navegador e redirecionado para o limite
    try:
        linha = int( linha )
    except:
        linha = 0
    try:
        coluna = int( coluna )
    except:
        coluna = 0
        
    teste_redirect = False
    if linha < settings.MAPS_MIN_X:
        linha = settings.MAPS_MIN_X
        teste_redirect = True
    if linha > settings.MAPS_MAX_X:
        linha = settings.MAPS_MAX_X
        teste_redirect = True
    if coluna < settings.MAPS_MIN_Y:
        coluna = settings.MAPS_MIN_Y
        teste_redirect = True
    if coluna > settings.MAPS_MAX_Y:
        coluna = settings.MAPS_MAX_Y
        teste_redirect = True
    
    if teste_redirect:
        return HttpResponseRedirect( reverse('viajar', args=[linha, coluna]) )



    
    #recupera uma lista de dados sobre os territorios a serem visualizados atualmente
    lugares = get_area(linha, coluna, 5)
    
    
    
    #sistema para incremento/decremento de coordenadas
    #para navegacao
    if linha + 5 <= settings.MAPS_MAX_X:
        next_linha = linha + 5
    else:
        next_linha = settings.MAPS_MAX_X
    if linha - 5 >= settings.MAPS_MIN_X:
        prev_linha = linha - 5
    else:
        prev_linha = settings.MAPS_MIN_X
    if coluna + 5 <= settings.MAPS_MAX_Y:
        next_coluna = coluna + 5
    else:
        next_coluna = settings.MAPS_MAX_Y
    if coluna - 5 >= settings.MAPS_MIN_Y:
        prev_coluna = coluna - 5
    else:
        prev_coluna = settings.MAPS_MIN_Y
        
    
    return render_to_response('mapa/minha_cidade.html', locals(), context_instance=RequestContext(request))





def minha_cidade(request):
    '''
    '''
    from mapa.functions import get_area, prepopulate_map
    from mapa.models import Terreno
    from tecnocracia import settings
    from django.core.urlresolvers import reverse
    from django.http import HttpResponseRedirect
    #from django.http import HttpResponse
    prepopulate_map()


    #neste bloco e feita a verificacao das coordenadas na navegacao
    #se extrapolar algum limite, o navegador e redirecionado para o limite
    linha = 0
    coluna = 0
        
    teste_redirect = False
    if linha < settings.LOCAL_MAPS_MIN_X:
        linha = settings.LOCAL_MAPS_MIN_X
        teste_redirect = True
    if linha > settings.LOCAL_MAPS_MAX_X:
        linha = settings.LOCAL_MAPS_MAX_X
        teste_redirect = True
    if coluna < settings.LOCAL_MAPS_MIN_Y:
        coluna = settings.LOCAL_MAPS_MIN_Y
        teste_redirect = True
    if coluna > settings.LOCAL_MAPS_MAX_Y:
        coluna = settings.LOCAL_MAPS_MAX_Y
        teste_redirect = True
    
    #if teste_redirect:
    #    return HttpResponseRedirect( reverse('viajar', args=[linha, coluna]) )


    #recupera uma lista de dados sobre os territorios a serem visualizados atualmente
    lugares = get_area(linha, coluna, 5)
    
    
    
    #sistema para incremento/decremento de coordenadas
    #para navegacao
    if linha + 5 <= settings.LOCAL_MAPS_MAX_X:
        next_linha = linha + 5
    else:
        next_linha = settings.LOCAL_MAPS_MAX_X
    if linha - 5 >= settings.LOCAL_MAPS_MIN_X:
        prev_linha = linha - 5
    else:
        prev_linha = settings.LOCAL_MAPS_MIN_X
    if coluna + 5 <= settings.LOCAL_MAPS_MAX_Y:
        next_coluna = coluna + 5
    else:
        next_coluna = settings.LOCAL_MAPS_MAX_Y
    if coluna - 5 >= settings.LOCAL_MAPS_MIN_Y:
        prev_coluna = coluna - 5
    else:
        prev_coluna = settings.LOCAL_MAPS_MIN_Y
        
    
    return render_to_response('mapa/minha_cidade.html', locals(), context_instance=RequestContext(request))


#view vazia por enquanto
def ajax_minha_cidade(request):
    
    return render_to_response('mapa/minha_cidade.html', locals(), context_instance=RequestContext(request))