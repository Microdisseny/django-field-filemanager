import os
import shutil

from django.conf import settings
from django.core.files import File
from django.test import TransactionTestCase

from documents.models import Document, Folder, Project


class DeleteTests(TransactionTestCase):

    def setUp(self):
        self.project = Project(**{'name': 'Customer  A'})
        self.project.save()

        self.folder = Folder(**{'name': 'Images', 'project': self.project})
        self.folder.save()

        files = ['2210571.jpg', 'images.docx']
        for file in files:
            path = 'tests/files/%s' % file
            f = open(path, 'rb')
            document = Document()
            document.folder = self.folder
            document.name = file
            document.file.save(name=document.name, content=File(f))
            document.save()
            document.save_thumbnail()
            f.close()

    def tearDown(self):
        Document.objects.all().delete()
        Folder.objects.all().delete()
        Project.objects.all().delete()
        for item in os.listdir(settings.MEDIA_ROOT):
            shutil.rmtree(os.path.join(settings.MEDIA_ROOT, item))

    def test_delete_project(self):
        document = Document.objects.all().first()
        base_upload_to = document.base_upload_to()
        path = os.path.join(settings.MEDIA_ROOT, base_upload_to)
        parent_base_upload_to = Document.parent_base_upload_to(document.folder)

        self.assertTrue(os.path.isdir(path))
        self.assertTrue(os.path.isdir(os.path.join(path, 'filemanager')))
        self.assertTrue(os.path.isdir(os.path.join(path, 'filemanager_thumbnails')))
        Project.objects.all().delete()

        self.assertFalse(os.path.isdir(path))
        path = os.path.join(settings.MEDIA_ROOT, base_upload_to)
        self.assertFalse(os.path.isdir(parent_base_upload_to))

    def test_delete_folder(self):
        document = Document.objects.all().first()
        base_upload_to = document.base_upload_to()
        path = os.path.join(settings.MEDIA_ROOT, base_upload_to)
        parent_base_upload_to = Document.parent_base_upload_to(document.folder)

        self.assertTrue(os.path.isdir(path))
        self.assertTrue(os.path.isdir(os.path.join(path, 'filemanager')))
        self.assertTrue(os.path.isdir(os.path.join(path, 'filemanager_thumbnails')))
        Folder.objects.all().delete()
        self.assertFalse(os.path.isdir(path))
        path = os.path.join(settings.MEDIA_ROOT, base_upload_to)
        self.assertFalse(os.path.isdir(parent_base_upload_to))

    def test_delete_documents(self):
        files = []
        documents = Document.objects.all()
        for document in documents:
            files.append(document.file.path)
            if document.thumbnail:
                files.append(document.thumbnail.path)
        self.assertTrue(len(files) == 3)
        for file in files:
            self.assertTrue(os.path.isfile(file))
        Document.objects.all().delete()
        for file in files:
            self.assertFalse(os.path.isfile(file))
