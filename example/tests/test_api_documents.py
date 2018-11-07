import os
import shutil

from django.conf import settings
from django.contrib.auth.models import User
from django.core.files import File
from django.test.utils import override_settings
from django.urls import reverse

from documents.models import Document, Folder
from rest_framework import status
from rest_framework.test import APITestCase


@override_settings(DEBUG=True)
class ApiDocumentsTests(APITestCase):

    def login(self):
        self.client.login(username='admin', password='admin')

    def setUp(self):
        self.admin_user = User.objects.create_superuser('admin', '', 'admin')
        self.login()

        self.folder = folder = Folder(**{'name': 'Projects'})
        folder.save()

    def tearDown(self):
        Document.objects.all().delete()
        Folder.objects.all().delete()
        for item in os.listdir(settings.MEDIA_ROOT):
            shutil.rmtree(os.path.join(settings.MEDIA_ROOT, item))

    def test_list(self):

        self.folder = Folder(**{'name': 'Images'})
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

        url = reverse('file_upload_view_list', args=['documents.Document', 'folder', self.folder.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

        url = reverse('file_upload_view_detail', args=['documents.Document', 'folder', self.folder.pk, files[0]])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], files[0])

    def test_post_image(self):
        url = reverse('file_upload_view_list', args=['documents.Document', 'folder', self.folder.pk])
        path = 'tests/files/2210571.jpg'
        f = open(path, 'rb')
        data = {'file': f, 'folder': self.folder.pk}
        response = self.client.post(url, data)
        f.close()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(
            response.data['name'], '2210571.jpg')
        self.assertTrue(
            response.data['file'].endswith('2210571.jpg'))
        self.assertFalse(
            response.data['thumbnail'] is None)

    def test_post_pdf(self):
        url = reverse('file_upload_view_list', args=['documents.Document', 'folder', self.folder.pk])
        path = 'tests/files/sample.pdf'
        f = open(path, 'rb')
        data = {'file': f, 'folder': self.folder.pk}
        response = self.client.post(url, data)
        f.close()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(
            response.data['name'], 'sample.pdf')
        self.assertTrue(
            response.data['file'].endswith('sample.pdf'))
        self.assertFalse(
            response.data['thumbnail'] is None)

    def test_delete(self):
        name = '2210571.jpg'
        url = reverse('file_upload_view_detail', args=['documents.Document', 'folder', self.folder.pk, name])
        path = 'tests/files/%s' % name
        f = open(path, 'rb')
        document = Document()
        document.folder = self.folder
        document.name = '2210571.jpg'
        document.file.save(name=document.name, content=File(f))
        document.save()
        f.close()
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
