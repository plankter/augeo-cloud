from django.conf.urls import patterns, include, url
from django.contrib import admin

import core.urls as core
import auctions.urls as auctions
import social.apps.django_app.urls as social
import profiles.urls as profiles
import events.urls as events

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'', include(core, namespace='core')),
    url(r'', include(auctions, namespace='auctions')),
    url('', include(social, namespace='social')),
    url(r'', include(profiles, namespace='profiles')),
    url(r'', include(events, namespace='events')),
)