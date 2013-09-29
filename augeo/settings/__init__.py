from split_settings.tools import optional, include
import os
import socket

if os.environ['DJANGO_SETTINGS_MODULE'] == 'augeo.settings':
    # must bypass this block if another settings module was specified
    include(
        'components/base.py',
        'components/debug.py',
        'components/db.py',
        'components/cache.py',
        'components/middleware.py',
        'components/static.py',
        'components/media.py',
        'components/templates.py',
        'components/email.py',
        'components/messages.py',
        'components/logging.py',
        'components/sessions.py',
        'components/security.py',
        'components/fixtures.py',
        'components/auth.py',
        'components/apps.py',

        'components/django-debug-toolbar.py',
        'components/django-storages.py',
        'components/python-social-auth.py',
        'components/cloudinary.py',
        'components/crispy-forms.py',
        'components/django-suit.py',

        # OVERRIDE SETTINGS

        # hostname-based override, in settings/env/ directory
        optional('env/%s.py' % socket.gethostname().split('.', 1)[0]),

        # local settings (do not commit to version control)
        optional(os.path.join(os.getcwd(), 'local_settings.py')),

        scope=locals()
    )