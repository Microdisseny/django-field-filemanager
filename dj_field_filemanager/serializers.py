import os

from django.urls import reverse

from rest_framework import serializers


def create_serializer(model, fields, read_only_fields):
    attrs = {
        '__module__': 'dj_field_filemanager',
        'Meta': type(str('Meta'), (object,),
                     {
                         'model': model,
                         'fields': fields,
                         'read_only_fields': read_only_fields
                         })
    }
    serializer = type(str('%s_serializer') % str(model._meta.db_table),
                      (serializers.ModelSerializer,), attrs)
    return serializer


class StorageSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    file = serializers.FileField()
    thumbnail = serializers.FileField(read_only=True)
    version = serializers.CharField(read_only=True)

    def __init__(self, *args, **kwargs):
        self.model = kwargs.pop('model', kwargs['model'])
        self.storage = self.model.get_storage()
        super().__init__(*args, **kwargs)

    def save(self, **kwargs):
        obj = self.model()
        obj.save(self.validated_data)
        obj.refresh()
        self.instance = obj

    def to_representation(self, obj):
        data = super().to_representation(obj)
        url = None
        if not('url' in self.model.storage_config):
            url = '%s?format=raw' % reverse(
                'storage_view_detail', args=[self.model.storage_config['code'], data['name']])
        else:
            url = self.storage.url(data['name'])
        data['file'] = self.context['request'].build_absolute_uri(url)
        if obj.thumbnail:
            thumbnail_name = os.path.basename(obj.thumbnail)
            url = self.context['request'].build_absolute_uri(
                self.model.get_thumbnail_storage().url(thumbnail_name))
            data['thumbnail'] = url
        return data
