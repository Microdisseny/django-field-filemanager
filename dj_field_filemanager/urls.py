from django.urls import path, re_path

from . import views
from .api import ModelViewSet, StorageViewSet

storage_list = StorageViewSet.as_view({'get': 'list', 'post': 'create'})
storage_detail = StorageViewSet.as_view({'get': 'retrieve', 'delete': 'destroy'})

model_list = ModelViewSet.as_view({'get': 'list', 'post': 'create'})
model_detail = ModelViewSet.as_view({'get': 'retrieve', 'delete': 'destroy'})

urlpatterns = [
    re_path(r'^(?P<model>[\w\.]+)/(?P<parent_field>[\w-]+)/(?P<parent_pk>[\d]+)/(?P<pk>.*)/$', model_detail,
            name='model_view_detail'),
    re_path(r'^(?P<model>[\w\.]+)/(?P<parent_field>[\w-]+)/(?P<parent_pk>[\d]+)/$', model_list,
            name='model_view_list'),

    re_path(r'^(?P<code>[\w\.]+)/(?P<pk>.*)/$', storage_detail, name='storage_view_detail'),
    re_path(r'^(?P<code>[\w\.]+)/$', storage_list, name='storage_view_list'),

    path(
        'filemanager/model/'
        '<str:label>/<str:model>/<int:parent_pk>/<str:field>/<path:file>',
        views.filemanager_model_server,
        {'thumbnail': False},
        'filemanager_model_url'
    ),
    path(
        'filemanager/model/thumbnail/'
        '<str:label>/<str:model>/<int:parent_pk>/<str:field>/<path:file>',
        views.filemanager_model_server,
        {'thumbnail': True},
        'filemanager_model_thumbnail_url'
    ),
    # http://localhost:8000/dj_field_filemanager/filemanager/storage/thumbnail/storage_file_example/aaa.pdf.thumbnail.jpg
    path(
        'filemanager/storage/thumbnail/'
        '<str:storage_code>/<path:file>',
        views.filemanager_storage_server,
        {'thumbnail': True},
        'filemanager_storage_thumbnail_url'
    ),
    path(
        'filemanager/storage/'
        '<str:storage_code>/<path:file>',
        views.filemanager_storage_server,
        {'thumbnail': False},
        'filemanager_storage_url'
    ),
]
