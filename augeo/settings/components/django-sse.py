from os import environ

# See: https://github.com/niwibe/django-sse
REDIS_SSEQUEUE_CONNECTION_SETTINGS = {
    'location': 'localhost:6379',
    'db': 0,
}