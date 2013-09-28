# See: https://docs.djangoproject.com/en/1.5/ref/settings/#authentication-backends
AUTHENTICATION_BACKENDS = (
    'social.backends.twitter.TwitterOAuth',
    'social.backends.facebook.FacebookOAuth2',

    'django.contrib.auth.backends.ModelBackend',
)

