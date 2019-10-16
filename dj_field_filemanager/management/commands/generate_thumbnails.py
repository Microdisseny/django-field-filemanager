import logging

from django.apps import apps
from django.core.management.base import BaseCommand

from dj_field_filemanager.models import DocumentModel


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Generates all thumbnails'

    def handle(self, *args, **options):
        for model in apps.get_models(include_auto_created=False):
            if issubclass(model, DocumentModel):
                for document in model.objects.all():
                    document.save_thumbnail(save=True)
