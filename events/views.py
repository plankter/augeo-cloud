from django.http import HttpResponse

from django_sse.redisqueue import RedisQueueView, send_event


class EventsView(RedisQueueView):
    def get_redis_channel(self):
        return "events_%s" % self.request.user.username


def ping(request):
    send_event("message", "Hi there!", 'events')
    return HttpResponse('Sent')