from django.conf.urls import patterns, include, url
from django.contrib import admin

import core.urls as core

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'', include(core, namespace='core')),
    url('', include('social.apps.django_app.urls', namespace='social')),
    url(r'', include('profiles.urls', namespace='profiles')),
)