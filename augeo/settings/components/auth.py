# See: https://docs.djangoproject.com/en/1.5/ref/settings/#authentication-backends
AUTH_USER_MODEL = 'auth.User'

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)

