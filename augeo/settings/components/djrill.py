from os import environ

# See: https://github.com/brack3t/Djrill
INSTALLED_APPS += (
    'djrill',
)

MANDRILL_API_KEY = environ['MANDRILL_APIKEY']
EMAIL_BACKEND = "djrill.mail.backends.djrill.DjrillBackend"