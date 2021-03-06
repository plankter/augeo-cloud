from os import environ

# See: https://github.com/omab/python-social-auth
INSTALLED_APPS += (
    'social.apps.django_app.default',
)

AUTHENTICATION_BACKENDS += (
    'social.backends.twitter.TwitterOAuth',
    'social.backends.facebook.FacebookOAuth2',
)

TEMPLATE_CONTEXT_PROCESSORS += (
    'social.apps.django_app.context_processors.backends',
    'social.apps.django_app.context_processors.login_redirect',
)

SOCIAL_AUTH_PROTECTED_USER_FIELDS = ['email',]

SOCIAL_AUTH_STRATEGY = 'social.strategies.django_strategy.DjangoStrategy'
SOCIAL_AUTH_STORAGE = 'social.apps.django_app.default.models.DjangoStorage'

SOCIAL_AUTH_TWITTER_KEY = environ['TWITTER_KEY']
SOCIAL_AUTH_TWITTER_SECRET = environ['TWITTER_SECRET']

SOCIAL_AUTH_FACEBOOK_KEY = environ['FACEBOOK_APP_KEY']
SOCIAL_AUTH_FACEBOOK_SECRET = environ['FACEBOOK_APP_SECRET']
SOCIAL_AUTH_FACEBOOK_SCOPE = ['email']