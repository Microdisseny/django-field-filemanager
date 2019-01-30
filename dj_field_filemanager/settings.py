from django.conf import settings

from .permissions import ModelHasPermission, StorageHasPermission
from .storage import OverwriteStorage

FIELD_FILEMANAGER_WIDTH = getattr(settings, 'FIELD_FILEMANAGER_WIDTH', 240)
FIELD_FILEMANAGER_HEIGHT = getattr(settings, 'FIELD_FILEMANAGER_HEIGHT', 240)
MEDIA_ROOT = getattr(settings, 'MEDIA_ROOT')

FIELD_FILEMANAGER_USE_VUE_JS = getattr(settings, 'FIELD_FILEMANAGER_USE_VUE_JS', True)

FIELD_FILEMANAGER_STORAGE = getattr(settings, 'FIELD_FILEMANAGER_STORAGE', OverwriteStorage)

FIELD_FILEMANAGER_API_PERMISSIONS = getattr(settings, 'FIELD_FILEMANAGER_API_PERMISSIONS', (ModelHasPermission,))

FIELD_FILEMANAGER_STORAGE_CONFIG = getattr(settings, 'FIELD_FILEMANAGER_STORAGE_CONFIG', [])

FIELD_FILEMANAGER_STORAGE_DEFAULT_STORAGE = 'django.core.files.storage.FileSystemStorage'

FIELD_FILEMANAGER_STORAGE_PERMISSIONS = getattr(
    settings, 'FIELD_FILEMANAGER_STORAGE_PERMISSIONS', (StorageHasPermission,))
