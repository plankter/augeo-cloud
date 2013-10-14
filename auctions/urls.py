from django.conf.urls import patterns, url

from .views import AuctionList, AuctionCreate, AuctionUpdate, AuctionDelete, AuctionDetail, BidView, AuctionTaggedList


urlpatterns = patterns('',
    url(r'auctions/$', AuctionList.as_view(), name='auction_list'),

    url(r'^auction/add/(?P<slug>[^\.]+)/$', AuctionCreate.as_view(), name='auction_add'),
    url(r'^auction/edit/(?P<slug>[^\.]+)/$', AuctionUpdate.as_view(), name='auction_edit'),
    url(r'^auction/delete/(?P<slug>[^\.]+)/$', AuctionDelete.as_view(), name='auction_delete'),

    url(r'^auction/bid/(?P<slug>[^\.]+)/$', BidView.as_view(), name='bid'),

    url(r'^auction/(?P<slug>[^\.]+)/$', AuctionDetail.as_view(), name='auction_detail'),

    url(r'^auctions/tag/(?P<tag>[^\.]+)/$', AuctionTaggedList.as_view(), name='tag_list'),
)