from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',

    url(r'^$', 'tecnocracia.frente.views.home', name='home'),

)
