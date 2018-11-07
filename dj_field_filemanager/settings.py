from django.conf import settings

from .storage import OverwriteStorage

FIELD_FILEMANAGER_WIDTH = getattr(settings, 'FIELD_FILEMANAGER_WIDTH', 240)
FIELD_FILEMANAGER_HEIGHT = getattr(settings, 'FIELD_FILEMANAGER_HEIGHT', 240)
MEDIA_ROOT = getattr(settings, 'MEDIA_ROOT')

FIELD_FILEMANAGER_USE_VUE_JS = getattr(settings, 'FIELD_FILEMANAGER_USE_VUE_JS', True)

FIELD_FILEMANAGER_STORAGE = getattr(settings, 'FIELD_FILEMANAGER_STORAGE', OverwriteStorage)
