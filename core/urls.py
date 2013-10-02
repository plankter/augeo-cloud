from django.conf.urls import patterns, url

from .views import ArtworkList, ArtworkCreate, ArtworkUpdate, ArtworkDelete, ArtworkDetail
from events.views import ping

urlpatterns = patterns('',
    url(r'^$', ArtworkList.as_view(), name='home'),
    url(r'ping/$', ping, name='ping'),
    url(r'artwork/add/$', ArtworkCreate.as_view(), name='artwork_add'),
    url(r'^artwork/edit/(?P<slug>[^\.]+)/$', ArtworkUpdate.as_view(), name='artwork_edit'),
    url(r'^artwork/delete/(?P<slug>[^\.]+)/$', ArtworkDelete.as_view(), name='artwork_delete'),
    url(r'^artwork/(?P<slug>[^\.]+)/$', ArtworkDetail.as_view(), name='artwork_detail'),
)