from django.conf.urls import patterns, url

from .views import ArtworkList, ArtworkCreate, ArtworkUpdate, ArtworkDelete, ArtworkDetail


urlpatterns = patterns('',
    url(r'^$', ArtworkList.as_view(), name='home'),
    url(r'artwork/add/$', ArtworkCreate.as_view(), name='artwork_add'),
    url(r'^artwork/(?P<slug>[-_\w]+)/$', ArtworkDetail.as_view(), name='artwork_detail'),
    url(r'^artwork/(?P<slug>[^\.]+)/edit/$', ArtworkUpdate.as_view(), name='artwork_edit'),
    url(r'^artwork/(?P<slug>[^\.]+)/delete/$', ArtworkDelete.as_view(), name='artwork_delete'),
)