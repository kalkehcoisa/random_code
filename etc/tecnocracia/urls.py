from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    
    url(r'^', include('tecnocracia.frente.urls')),
    url(r'^mapas/', include('tecnocracia.mapa.urls')),
    
    #url(r'^battles/', include('tecnocracia.battle_system.urls')),


    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

from django.conf import settings


urlpatterns += patterns('django.views.static',
(r'^static_media/(?P<path>.*)$',
    'serve', {
    'document_root': settings.MEDIA_ROOT,
    'show_indexes': True }),)

'''
urlpatterns += patterns('django.views.static',
(r'^media/(?P<path>.*)$',
    'serve', {
    'document_root': '/home/danielcj/webapps/mae/lib/python2.7/django/contrib/admin/media/',
    'show_indexes': True }),)
'''
