from os import environ
from os.path import abspath, dirname, normpath, join

# Absolute filesystem path to the Django project directory:
DJANGO_ROOT = normpath(join(dirname(dirname(abspath(__file__))), '..'))

# Site name:
SITE_NAME = 'augeo'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#admins
ADMINS = (
    ('Anton Rau', 'anton.rau@gmail.com'),
)

# See: https://docs.djangoproject.com/en/dev/ref/settings/#managers
MANAGERS = ADMINS

# See: https://docs.djangoproject.com/en/dev/ref/settings/#time-zone
TIME_ZONE = 'Europe/Zurich'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#language-code
LANGUAGE_CODE = 'en-us'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#site-id
SITE_ID = 1

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-i18n
USE_I18N = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-l10n
USE_L10N = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-tz
USE_TZ = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
SECRET_KEY = environ['SECRET_KEY']

# See: https://docs.djangoproject.com/en/dev/ref/settings/#root-urlconf
ROOT_URLCONF = '%s.urls' % SITE_NAME

# See: https://docs.djangoproject.com/en/dev/ref/settings/#wsgi-application
WSGI_APPLICATION = 'augeo.wsgi.application'

# See: https://docs.djangoproject.com/en/1.5/ref/settings/
LOGIN_URL = '/'
LOGIN_REDIRECT_URL = '/'