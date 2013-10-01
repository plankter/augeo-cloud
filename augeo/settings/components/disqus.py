from os import environ

# See: http://django-disqus.readthedocs.org/en/latest/installation.html
INSTALLED_APPS += (
    'disqus',
)

DISQUS_API_KEY = environ['DISQUS_API_KEY']
DISQUS_WEBSITE_SHORTNAME = 'augeo'