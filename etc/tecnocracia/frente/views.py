#-*- coding: utf-8 -*-

from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.utils.encoding import smart_str


def home(request):
    '''
    '''
    
    return render_to_response('front_pages/home.html', locals(), context_instance=RequestContext(request))