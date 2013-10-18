from django.conf.urls import patterns, include, url
from django.contrib import admin

from rest_framework import routers

from core.api import ArtworkViewSet
from auctions.api import AuctionViewSet

import core.urls as core
import auctions.urls as auctions
import social.apps.django_app.urls as social
import profiles.urls as profiles
import events.urls as events
import rest_framework.urls as rest_framework

admin.autodiscover()


# Routers provide an easy way of automatically determining the URL conf
router = routers.DefaultRouter()
router.register(r'artworks', ArtworkViewSet, base_name='artwork')
router.register(r'auctions', AuctionViewSet, base_name='auction')


urlpatterns = patterns('',
    url(r'^api/v1/', include(router.urls)),

    url(r'^admin/', include(admin.site.urls)),
    url(r'', include(core, namespace='core')),
    url(r'', include(auctions, namespace='auctions')),
    url('', include(social, namespace='social')),
    url(r'', include(profiles, namespace='profiles')),
    url(r'', include(events, namespace='events')),

    url(r'^api-auth/', include(rest_framework, namespace='rest_framework'))
)