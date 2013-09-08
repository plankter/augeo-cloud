from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'accounts/login.html'}, name='login'),
    url(r'^logout/$', 'accounts.views.logout_user', name='logout'),
)