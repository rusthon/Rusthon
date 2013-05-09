from django.conf.urls import patterns, include, url
from django.shortcuts import render


def index(request):
    return render(request, 'index.html')


urlpatterns = patterns('',
    url(r'^$', index),
)
