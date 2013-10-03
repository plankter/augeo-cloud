from os import environ
from django.http import HttpResponse

from Pubnub import Pubnub


pubnub = Pubnub(
    environ['PUBNUB_PUBLISH_KEY'],      # PUBLISH_KEY
    environ['PUBNUB_SUBSCRIBE_KEY'],    # SUBSCRIBE_KEY
    None,                               # SECRET_KEY
    False                               # SSL_ON?
)


def ping(request):
    info = pubnub.publish({
        'channel': 'augeo',
        'message': {
            'text': 'Hello my <strong>World</strong>'
        }
    })
    return HttpResponse(info)
