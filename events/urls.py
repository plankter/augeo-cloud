from django.conf.urls import patterns, url

from .views import ping

urlpatterns = patterns('',
    url(r'ping/$', ping, name='ping'),
)