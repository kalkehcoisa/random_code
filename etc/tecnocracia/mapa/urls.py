from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('',


    url(r'^world_view$', 'tecnocracia.mapa.views.visao_geral', {}, 'visao_geral'),
    
    url(r'^world_travel/{0,1}$', 'tecnocracia.mapa.views.viajar', {'linha':None, 'coluna':None}, 'viajar'),
    url(r'^world_travel/(?P<linha>\d+)/$', 'tecnocracia.mapa.views.viajar', {'coluna':None}, 'viajar'),
    url(r'^world_travel/(?P<linha>-{0,1}\d+)/(?P<coluna>-{0,1}\d+)/$', 'tecnocracia.mapa.views.viajar', {}, 'viajar'),
    
    
    
    
    url(r'^my_city$', 'tecnocracia.mapa.views.minha_cidade', {}, 'minha_cidade'),
    url(r'^my_city/(?P<linha>-{0,1}\d+)/(?P<coluna>-{0,1}\d+)/$', 'tecnocracia.mapa.views.ajax_minha_cidade', {}, 'ajax_mover_minha_cidade'),
    
    
)
