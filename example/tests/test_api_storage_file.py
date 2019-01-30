import os
import shutil

from django.conf import settings
from django.contrib.auth.models import User
from django.test.utils import override_settings
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase


@override_settings(DEBUG=True)
class ApiStorageFileTests(APITestCase):

    def login(self):
        self.client.login(username='admin', password='admin')

    def setUp(self):
        self.admin_user = User.objects.create_superuser('admin', '', 'admin')
        self.directory = os.path.join(
            settings.MEDIA_ROOT, 'storage_file_example')
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)

        self.directory_thumbnails = os.path.join(
            settings.MEDIA_ROOT, 'storage_file_thumbnails_example')
        if not os.path.exists(self.directory_thumbnails):
            os.makedirs(self.directory_thumbnails)

    def tearDown(self):
        for item in os.listdir(settings.MEDIA_ROOT):
            shutil.rmtree(os.path.join(settings.MEDIA_ROOT, item))

    def test_list(self):
        self.login()
        files = ['2210571.jpg', 'images.docx', 'rgba1px.png']
        for name in files:
            src = 'tests/files/%s' % name
            dst = '%s/%s' % (self.directory, name)
            shutil.copyfile(src, dst)
            if not name.endswith('.docx'):
                thumbnail = '%s/%s.thumbnail.jpg' % (self.directory_thumbnails, name)
                shutil.copyfile(src, thumbnail)

        url = reverse('storage_view_list', args=['test'])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), len(files))

        for i in range(len(response.data)):
            item = response.data[i]
            if item['name'].split('.')[-1] in ('jpg', 'png'):
                self.assertEqual(item['thumbnail'].split('/')[-1], ('%s.thumbnail.jpg' % item['file']).split('/')[-1])
            else:
                self.assertEqual(item['thumbnail'], None)

    def test_post_image(self):
        self.login()
        url = reverse('storage_view_list', args=['test'])
        path = 'tests/files/2210571.jpg'
        f = open(path, 'rb')
        data = {'file': f}
        response = self.client.post(url, data)
        f.close()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(
            response.data['name'], '2210571.jpg')
        self.assertTrue(
            response.data['file'].endswith('2210571.jpg'))
        self.assertFalse(
            response.data['thumbnail'] is None)

    def test_post_image_bad_name(self):
        self.login()
        url = reverse('storage_view_list', args=['test'])
        path = 'tests/files/bad name.jpg'
        f = open(path, 'rb')
        data = {'file': f}
        response = self.client.post(url, data)
        f.close()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(
            response.data['name'], 'bad_name.jpg')
        self.assertTrue(
            response.data['file'].endswith('bad_name.jpg'))
        self.assertFalse(
            response.data['thumbnail'] is None)

    def test_post_pdf(self):
        self.login()
        url = reverse('storage_view_list', args=['test'])
        path = 'tests/files/sample.pdf'
        f = open(path, 'rb')
        data = {'file': f}
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
        self.login()
        name = '2210571.jpg'
        src = 'tests/files/%s' % name
        file = '%s/%s' % (self.directory, name)
        shutil.copyfile(src, file)
        thumbnail = '%s/%s.thumbnail.jpg' % (self.directory_thumbnails, name)
        shutil.copyfile(src, thumbnail)
        self.assertTrue(os.path.exists(file))
        self.assertTrue(os.path.exists(thumbnail))
        url = reverse('storage_view_detail', args=['test', name])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(os.path.exists(file))
        self.assertFalse(os.path.exists(thumbnail))

    def test_get(self):
        self.login()
        name = '2210571.jpg'
        src = 'tests/files/%s' % name
        file = '%s/%s' % (self.directory, name)
        shutil.copyfile(src, file)
        thumbnail = '%s/%s.thumbnail.jpg' % (self.directory_thumbnails, name)
        shutil.copyfile(src, thumbnail)
        self.assertTrue(os.path.exists(file))
        self.assertTrue(os.path.exists(thumbnail))
        url = reverse('storage_view_detail', args=['test', name])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertTrue(
            response.data['name'], '2210571.jpg')
        self.assertTrue(
            response.data['file'].endswith('2210571.jpg'))
        self.assertTrue(
            response.data['thumbnail'].endswith('2210571.jpg.thumbnail.jpg'))

    def test_not_found(self):
        self.login()
        url = reverse('storage_view_detail', args=['test', 'aaa.png'])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_permission_denied(self):
        url = reverse('storage_view_list', args=['test'])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
