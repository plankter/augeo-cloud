from os import environ

def get_cache():
    try:
        environ['MEMCACHE_SERVERS'] = environ['MEMCACHIER_SERVERS'].replace(',', ';')
        environ['MEMCACHE_USERNAME'] = environ['MEMCACHIER_USERNAME']
        environ['MEMCACHE_PASSWORD'] = environ['MEMCACHIER_PASSWORD']
        return {
            'default': {
                'BACKEND': 'django_pylibmc.memcached.PyLibMCCache',
                'TIMEOUT': 500,
                'BINARY': True,
                'OPTIONS': {'tcp_nodelay': True}
            }
        }
    except:
        return {
            'default': {
                'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'
            }
        }

# See: https://docs.djangoproject.com/en/dev/ref/settings/#caches
CACHES = get_cache()