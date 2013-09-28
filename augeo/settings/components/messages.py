# See: https://docs.djangoproject.com/en/1.5/ref/settings/#message-tags
from django.contrib.messages import constants as messages

MESSAGE_TAGS = {
    messages.WARNING: 'alert',
    messages.ERROR: 'alert alert-error',
    messages.SUCCESS: 'alert alert-success',
    messages.INFO: 'alert alert-info',
}