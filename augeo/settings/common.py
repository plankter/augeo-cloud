# Common Django settings for augeo project.

from os import environ
from os.path import abspath, basename, dirname, join, normpath
from sys import path


########## PATH CONFIGURATION
# Absolute filesystem path to the Django project directory:
DJANGO_ROOT = dirname(dirname(abspath(__file__)))

# Absolute filesystem path to the top-level project folder:
SITE_ROOT = dirname(DJANGO_ROOT)

# Site name:
SITE_NAME = basename(DJANGO_ROOT)

# Add our project to our pythonpath, this way we don't need to type our project
# name in our dotted import paths:
path.append(DJANGO_ROOT)
########## END PATH CONFIGURATION


########## MANAGER CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#admins
ADMINS = (
	('Anton Rau', 'anton.rau@gmail.com'),
)

# See: https://docs.djangoproject.com/en/dev/ref/settings/#managers
MANAGERS = ADMINS
########## END MANAGER CONFIGURATION


########## GENERAL CONFIGURATION
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
########## END GENERAL CONFIGURATION


########## MEDIA CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#media-root
MEDIA_ROOT = normpath(join(DJANGO_ROOT, 'media'))

# See: https://docs.djangoproject.com/en/dev/ref/settings/#media-url
MEDIA_URL = '/media/'
########## END MEDIA CONFIGURATION


########## STATIC FILE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-root
STATIC_ROOT = normpath(join(DJANGO_ROOT, 'static'))

# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-url
STATIC_URL = '/static/'

# See: https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#std:setting-STATICFILES_DIRS
STATICFILES_DIRS = (
	normpath(join(DJANGO_ROOT, 'static')),
)

# See: https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#staticfiles-finders
STATICFILES_FINDERS = (
	'django.contrib.staticfiles.finders.FileSystemFinder',
	'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)
########## END STATIC FILE CONFIGURATION


########## SECRET CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
SECRET_KEY = environ.get('SECRET_KEY', 'NO SECRETS!')
########## END SECRET CONFIGURATION


########## FIXTURE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-FIXTURE_DIRS
FIXTURE_DIRS = (
	normpath(join(DJANGO_ROOT, 'fixtures')),
)
########## END FIXTURE CONFIGURATION


########## TEMPLATE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#template-context-processors
TEMPLATE_CONTEXT_PROCESSORS = (
	'django.contrib.auth.context_processors.auth',
	'django.core.context_processors.debug',
	'django.core.context_processors.i18n',
	'django.core.context_processors.media',
	'django.core.context_processors.static',
	'django.core.context_processors.tz',
	'django.contrib.messages.context_processors.messages',
	'django.core.context_processors.request',

	'social.apps.django_app.context_processors.backends',
	'social.apps.django_app.context_processors.login_redirect',

	'core.context_processors.consts',
)

# See: https://docs.djangoproject.com/en/dev/ref/settings/#template-loaders
TEMPLATE_LOADERS = (
	'django.template.loaders.filesystem.Loader',
	'django.template.loaders.app_directories.Loader',
)

# See: https://docs.djangoproject.com/en/dev/ref/settings/#template-dirs
TEMPLATE_DIRS = (
	normpath(join(DJANGO_ROOT, 'templates')),
	normpath(join(DJANGO_ROOT, 'templates', 'core')),
)
########## END TEMPLATE CONFIGURATION


########## MIDDLEWARE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#middleware-classes
MIDDLEWARE_CLASSES = (
	# Default Django middleware.
	'django.middleware.common.CommonMiddleware',
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	'django.middleware.clickjacking.XFrameOptionsMiddleware',
)
########## END MIDDLEWARE CONFIGURATION


########## URL CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#root-urlconf
ROOT_URLCONF = '%s.urls' % SITE_NAME
########## END URL CONFIGURATION


########## APP CONFIGURATION
DJANGO_APPS = (
	# Default Django apps:
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.sites',
	'django.contrib.messages',
	'django.contrib.staticfiles',

	# Useful template tags:
	'django.contrib.humanize',

	# Admin panel and documentation:
	'django.contrib.admin',
	'django.contrib.admindocs',
)

THIRD_PARTY_APPS = (
	# Database migration helpers:
	'south',

	'social.apps.django_app.default',
	'suit',
	'cloudinary',
	'pure_pagination',
	'crispy_forms',
	'taggit',
)

LOCAL_APPS = (
	'profiles',
	'core',
)

# See: https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS
########## END APP CONFIGURATION


########## LOGGING CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#logging
LOGGING = {
	'version': 1,
	'disable_existing_loggers': False,
	'filters': {
		'require_debug_false': {
			'()': 'django.utils.log.RequireDebugFalse'
		}
	},
	'handlers': {
		'mail_admins': {
			'level': 'ERROR',
			'filters': ['require_debug_false'],
			'class': 'django.utils.log.AdminEmailHandler'
		},
		'console': {
			'level': 'DEBUG',
			'class': 'logging.StreamHandler'
		}
	},
	'loggers': {
		'django.request': {
			'handlers': ['mail_admins', 'console'],
			'level': 'ERROR',
			'propagate': True,
		},
	}
}
########## END LOGGING CONFIGURATION


########## WSGI CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#wsgi-application
WSGI_APPLICATION = 'augeo.wsgi.application'
########## END WSGI CONFIGURATION


########## MESSAGES CONFIGURATION
# See: https://docs.djangoproject.com/en/1.5/ref/settings/#message-tags
from django.contrib.messages import constants as messages

MESSAGE_TAGS = {
	messages.WARNING: 'alert',
	messages.ERROR: 'alert alert-error',
	messages.SUCCESS: 'alert alert-success',
	messages.INFO: 'alert alert-info',
}
########## END MESSAGES CONFIGURATION


########## SESSIONS CONFIGURATION
# See: https://docs.djangoproject.com/en/1.5/ref/settings/#session-engine
SESSION_ENGINE = "django.contrib.sessions.backends.cached_db"
########## END SESSIONS CONFIGURATION


########## AUTHENTICATION CONFIGURATION
# See: https://docs.djangoproject.com/en/1.5/ref/settings/#authentication-backends
AUTHENTICATION_BACKENDS = (
	'social.backends.twitter.TwitterOAuth',
	'social.backends.facebook.FacebookOAuth2',

	'django.contrib.auth.backends.ModelBackend',
)
########## END AUTHENTICATION CONFIGURATION


########## REDIRECTS CONFIGURATION
# See: https://docs.djangoproject.com/en/1.5/ref/settings/
LOGIN_URL = '/'
LOGIN_REDIRECT_URL = '/'
URL_PATH = ''
########## END REDIRECTS CONFIGURATION



########## django-suit CONFIGURATION
# See: http://django-suit.readthedocs.org/en/develop/
SUIT_CONFIG = {
	# header
	'ADMIN_NAME': 'Augeo',
	# 'HEADER_DATE_FORMAT': 'l, j. F Y',
	# 'HEADER_TIME_FORMAT': 'H:i',
}
########## END django-suit CONFIGURATION


########## python-social-auth CONFIGURATION
# See: https://github.com/omab/python-social-auth
SOCIAL_AUTH_STRATEGY = 'social.strategies.django_strategy.DjangoStrategy'
SOCIAL_AUTH_STORAGE = 'social.apps.django_app.default.models.DjangoStorage'

SOCIAL_AUTH_TWITTER_KEY = environ['TWITTER_KEY']
SOCIAL_AUTH_TWITTER_SECRET = environ['TWITTER_SECRET']

SOCIAL_AUTH_FACEBOOK_KEY = environ['FACEBOOK_APP_KEY']
SOCIAL_AUTH_FACEBOOK_SECRET = environ['FACEBOOK_APP_SECRET']
SOCIAL_AUTH_FACEBOOK_SCOPE = ['email']
########## END python-social-auth CONFIGURATION


########## Cloudinary CONFIGURATION
# See: http://cloudinary.com/documentation/django_integration#getting_started_guide
import cloudinary
cloudinary.config(
	cloud_name=environ['CLOUDINARY_CLOUD_NAME'],
	api_key=environ['CLOUDINARY_API_KEY'],
	api_secret=environ['CLOUDINARY_API_SECRET']
)
########## END Cloudinary CONFIGURATION


########## crispy_forms CONFIGURATION
# See: http://django-crispy-forms.readthedocs.org/en/latest/
CRISPY_TEMPLATE_PACK = 'bootstrap3'
########## END crispy_forms CONFIGURATION