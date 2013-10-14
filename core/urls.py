from django.conf.urls import patterns, url

from .views import ArtworkList, ArtworkCreate, ArtworkUpdate, ArtworkDelete, ArtworkDetail, ContactFormView, ArtworkTaggedList

urlpatterns = patterns('',
    url(r'^$', ArtworkList.as_view(), name='home'),
    url(r'contact/$', ContactFormView.as_view(), name='contact'),
    url(r'artwork/add/$', ArtworkCreate.as_view(), name='artwork_add'),
    url(r'^artwork/edit/(?P<slug>[^\.]+)/$', ArtworkUpdate.as_view(), name='artwork_edit'),
    url(r'^artwork/delete/(?P<slug>[^\.]+)/$', ArtworkDelete.as_view(), name='artwork_delete'),
    url(r'^artwork/(?P<slug>[^\.]+)/$', ArtworkDetail.as_view(), name='artwork_detail'),
    url(r'^artworks/tag/(?P<tag>[^\.]+)/$', ArtworkTaggedList.as_view(), name='tag_list'),
)