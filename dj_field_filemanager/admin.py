import warnings

from .admin_mixins import FieldFilemanagerAdminMixin


class FieldFilemanagerAdmin(FieldFilemanagerAdminMixin):
    def __init__(self, *args, **kwargs):
        warnings.warn(
            'FieldFilemanagerAdmin is deprecated; use FieldFilemanagerAdminMixin.',
            DeprecationWarning
        )
        super().__init__(*args, **kwargs)
