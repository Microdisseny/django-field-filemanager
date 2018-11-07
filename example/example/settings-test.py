import os
import tempfile

DEBUG = True

DATABASES['default'] = {  # noqa
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': ':memory',
}
# DATABASES['default']['OPTIONS'] = dict(timeout=30)


MEDIA_ROOT = os.path.join(tempfile.TemporaryDirectory().name, 'media')
