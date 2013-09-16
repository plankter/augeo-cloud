from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'augeo.views.home', name='home'),
    # url(r'^augeo/', include('augeo.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', TemplateView.as_view(template_name='base.html'), name='home'),
    url('', include('social.apps.django_app.urls', namespace='social')),
    url(r'', include('accounts.urls', namespace='accounts')),
    #url(r'', include('pinry.core.urls', namespace='core')),
    #url(r'', include('pinry.users.urls', namespace='users')),
)
