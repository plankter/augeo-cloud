from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

import gallery.views as gallery

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),

    # URL for listing all images:
    url(r'^$', gallery.PhotoList.as_view(), name='home'),
    url(r'^list$', gallery.PhotoList.as_view()),
    # The direct upload functionality reports to this URL when an image is uploaded.
    url(r'^upload/complete$', gallery.direct_upload_complete),

    url('', include('social.apps.django_app.urls', namespace='social')),
    url(r'', include('accounts.urls', namespace='accounts')),
    #url(r'', include('pinry.core.urls', namespace='core')),
    #url(r'', include('pinry.users.urls', namespace='users')),
)
