from django.conf.urls.defaults import *

urlpatterns = patterns('gouache.django_cart.views',

    (r'^cart/$', 'cart_list', {}, 'cart_list'),
    (r'^cart/add/$', 'cart_add', {}, 'cart_add'),
    (r'^cart/remove/(?P<produto_id>\d+)/$', 'cart_remove', {}, 'cart_remove'),
    
)


#ajax views
urlpatterns += patterns('gouache.django_cart.ajax',

    (r'^cart/add/$', 'add', {}, 'ajax_cart_add'),
    (r'^cart/remove/$', 'remove', {}, 'ajax_cart_remove'),

    (r'^cart/update/$', 'update', {}, 'ajax_cart_update'),

)