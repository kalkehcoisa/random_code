from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    (r'^login/$', 'rugby_django.login.views.rugby_login', {}, 'login'),
    (r'^logout/$', 'rugby_django.login.views.rugby_logout', {}, 'logout'),

    (r'^$', 'rugby_django.blog.views.index', {}, 'index'),



    #(r'^common/companies/logo/(?P<id>\d+)$', 'fgv_ghg.common.views.companieslogo', {}, 'commoncompanieslogo'),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('django.views.static',
(r'^static_media/(?P<path>.*)$',
    'serve', {
    'document_root': 'd:/meus/rugby_django/media/',
    'show_indexes': True }),)