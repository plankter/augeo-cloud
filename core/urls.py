from django.conf.urls import patterns, url

from .views import ArtworkList, ArtworkCreate, ArtworkUpdate, ArtworkDelete, direct_upload_complete


urlpatterns = patterns('',
    url(r'^$', ArtworkList.as_view(), name='home'),
    url(r'^artworks$', ArtworkList.as_view(), name='artworks'),
    url(r'artwork/add/$', ArtworkCreate.as_view(), name='artwork_add'),
    url(r'artwork/(?P<pk>\d+)/$', ArtworkUpdate.as_view(), name='artwork_update'),
    url(r'artwork/(?P<pk>\d+)/delete/$', ArtworkDelete.as_view(), name='artwork_delete'),
    # The direct upload functionality reports to this URL when an image is uploaded.
    url(r'^upload/complete$', direct_upload_complete, name='upload_complete'),
)