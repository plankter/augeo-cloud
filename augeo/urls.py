from django.conf.urls import patterns, include, url
from django.contrib import admin

import core.views as core

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),

    # URL for listing all images:
    url(r'^$', core.PhotoList.as_view(), name='home'),
    url(r'^list$', core.PhotoList.as_view()),
    # The direct upload functionality reports to this URL when an image is uploaded.
    url(r'^upload/complete$', core.direct_upload_complete),

    url('', include('social.apps.django_app.urls', namespace='social')),
    url(r'', include('accounts.urls', namespace='accounts')),
    #url(r'', include('pinry.core.urls', namespace='core')),
    #url(r'', include('pinry.users.urls', namespace='users')),
)
