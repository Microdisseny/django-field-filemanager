import io
import os
import uuid

from django.core.files.base import ContentFile
from django.db import models
from django.utils.translation import ugettext_lazy as _

import pdf2image
from PIL import Image

from . import settings


def _thumbnail_upload_to(instance, filename):
    return instance.thumbnail_upload_to(filename)


def _upload_to(instance, filename):
    return instance.upload_to(filename)


class DocumentModel(models.Model):
    ALLOWED_IMAGE_FORMATS = ('JPEG', 'PNG')
    EXTENSIONS = {
        'JPEG': 'jpg',
        'PNG': 'png',
    }
    PNG_SUPPORTED_MODES = ('1', 'L', 'RGB', 'RGBA')

    # Parent attribute name
    document_parent = None
    width = None
    height = None

    name = models.CharField(_('Name'), max_length=255, blank=True)
    file = models.FileField(_('File'), max_length=255, upload_to=_upload_to,
                            storage=settings.FIELD_FILEMANAGER_STORAGE())
    thumbnail = models.FileField(_('Thumbnail'), max_length=255, blank=True,
                                 null=True, upload_to=_thumbnail_upload_to,
                                 storage=settings.FIELD_FILEMANAGER_STORAGE())

    @classmethod
    def get_parent(cls):
        if cls.document_parent is None:
            raise Exception("'document_parent' ForeignKey field is not defined")
        return cls.document_parent

    @classmethod
    def parent_base_upload_to(cls, parent):
        """
        Returns the desired the base path for parent_model.

        By default it's 'app_label/parent_model/parent_rel_id' where:
          - app_label is the parent's app label
          - parent_model is the model name of the parent model
          - parent_rel_id is the identity of the parent as it is on the foreign key (usually the pk)
        """
        return '%s/%s/%s' % (parent._meta.app_label, parent._meta.model_name, parent.pk)

    def base_upload_to(self):
        """
        Returns the desired the base path for current model.

        By default it's 'app_label/parent_model/parent_rel_id/current' where:
          - app_label is the parent's app label
          - parent_model is the model name of the parent model
          - parent_rel_id is the identity of the parent as it is on the foreign key (usually the pk)
          - current model name
        """
        parent = getattr(self, (self.get_parent()))
        remote = self._meta.get_field(self.get_parent()).remote_field.name
        return '%s/%s' % (self.parent_base_upload_to(parent), remote)

    @classmethod
    def check_delete_parent_folder(cls, parent):
        """
        Check if the parent folder hasn't files and can be deleted
        """
        folder = os.path.join(
            settings.MEDIA_ROOT, cls.parent_base_upload_to(parent))

        def rmdir(target):
            items = os.listdir(target)
            if len(items) == 0:
                os.rmdir(target)
            else:
                for item in items:
                    path = os.path.join(target, item)
                    if not os.path.isdir(path):
                        msg = 'The folder %s contains some file' % path
                        raise FolderNotEmptyException(msg)
                for item in items:
                    path = os.path.join(target, item)
                    rmdir(path)
                os.rmdir(target)

        try:
            rmdir(folder)
        except Exception as e:
            print(e)

    def deferred_post_delete(self):
        """
        Called from transaction.on_commit.
        """
        if self.file and os.path.isfile(self.file.path):
            self.file.delete(save=False)
        if self.thumbnail and os.path.isfile(self.thumbnail.path):
            self.thumbnail.delete(save=False)

    def get_thumbnail_height(self):
        return self.height or settings.FIELD_FILEMANAGER_HEIGHT

    def get_thumbnail_width(self):
        return self.width or settings.FIELD_FILEMANAGER_WIDTH

    def save_thumbnail(self, save=True):
        """
        Generates a document thumbnail
        """
        modified = False
        if self.thumbnail:
            self.thumbnail.delete(save=False)
            modified = True

        im = None
        format = None
        if not self.file:
            pass
        elif self.file.name.lower().endswith('.pdf'):
            file = self.file
            file.open()
            images = pdf2image.convert_from_bytes(file.read(), first_page=1, last_page=1)
            if len(images) > 0:
                im = images[0]
                format = 'JPEG'
        else:
            try:
                im = Image.open(self.file)
                # Keep the same format if it's OK for us
                if im.format in self.ALLOWED_IMAGE_FORMATS:
                    format = im.format
                else:
                    # Convert it into PNG
                    if im.mode not in self.PNG_SUPPORTED_MODES:
                        # Force a valid PNG mode (RGB)
                        im = im.convert('RGBA')
                    format = 'PNG'
            except Exception:
                # not an image or unsupported
                im = None

        if im:
            # generate thumbnail
            size = (self.get_thumbnail_width(), self.get_thumbnail_height())
            im.thumbnail(size, Image.ANTIALIAS)
            buffer = io.BytesIO()
            im.save(buffer, format=format)

            # save thumbnail
            buffer.seek(0)
            bytes = buffer.read()
            if format in self.EXTENSIONS:
                extension = self.EXTENSIONS[format]
            else:
                extension = format.lower()
            filename = '%s.%s' % (uuid.uuid4(), extension)
            self.thumbnail.save(name=filename, content=ContentFile(bytes))
            modified = True

        if modified and save:
            self.save()

    def thumbnail_upload_to(self, filename):
        """
        Returns then path for thumbnail image
        """
        base_path = self.base_upload_to()
        return '%s/%s/%s' % (base_path, 'filemanager_thumbnails', filename)

    def upload_to(self, filename):
        """
        Returns the path for document
        """
        base_path = self.base_upload_to()
        return '%s/%s/%s' % (base_path, 'filemanager', filename)

    class Meta:
        abstract = True


class FolderNotEmptyException(Exception):
    pass
