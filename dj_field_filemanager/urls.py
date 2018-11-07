try:
    from django.urls import re_path
except Exception:
    from django.conf.urls import url as re_path

from .api import FileViewSet

file_list = FileViewSet.as_view({'get': 'list', 'post': 'create'})
file_detail = FileViewSet.as_view(
    {'get': 'retrieve', 'delete': 'destroy'})


urlpatterns = [
    re_path(r'^(?P<model>[\w\.]+)/(?P<parent_field>[\w-]+)/(?P<parent_pk>[\d]+)/(?P<pk>.*)/$', file_detail,
            name='file_upload_view_detail'),
    re_path(r'^(?P<model>[\w\.]+)/(?P<parent_field>[\w-]+)/(?P<parent_pk>[\d]+)/$', file_list,
            name='file_upload_view_list'),
]
