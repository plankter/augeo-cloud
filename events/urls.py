from django.conf.urls import patterns, url
from django_sse.redisqueue import RedisQueueView

from .views import EventsView


urlpatterns = patterns('',
    url(r'^events/$', RedisQueueView.as_view(redis_channel="events"), name='events'),
)