# See: https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ['.herokuapp.com']

# See: https://docs.djangoproject.com/en/1.5/ref/settings/#secure-proxy-ssl-header
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# See: https://docs.djangoproject.com/en/1.5/ref/settings/#internal-ips
INTERNAL_IPS = ('127.0.0.1',)
