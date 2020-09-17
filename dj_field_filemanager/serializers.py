from urllib.parse import urljoin

from django.urls import reverse

from rest_framework import serializers


class ModelSerializer(serializers.ModelSerializer):
    def to_representation(self, obj):
        data = super().to_representation(obj)
        data['file'] = obj.file_url(self.context['request'])
        data['thumbnail'] = obj.thumbnail_url(self.context['request'])
        return data


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
                      (ModelSerializer,), attrs)
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
        data['file'] = None
        data['thumbnail'] = None

        storage_config = getattr(self.model, 'storage_config')
        if obj.name:
            if 'url' in storage_config:
                url = urljoin(storage_config['url'], obj.name)
                if not(url.lower().startswith('http://') or url.lower().startswith('https://')):
                    url = self.context['request'].build_absolute_uri(url)
            else:
                name = 'filemanager_storage_url'
                partial = reverse(name, args=(storage_config['code'], obj.name))
                url = self.context['request'].build_absolute_uri(partial)
            data['file'] = url
        if obj.thumbnail and 'thumbnail' in storage_config:
            if 'url' in storage_config['thumbnail']:
                url = urljoin(storage_config['thumbnail']['url'], obj.thumbnail)
                if not(url.lower().startswith('http://') or url.lower().startswith('https://')):
                    url = self.context['request'].build_absolute_uri(url)
            else:
                name = 'filemanager_storage_thumbnail_url'
                partial = reverse(name, args=(storage_config['code'], obj.thumbnail))
                url = self.context['request'].build_absolute_uri(partial)
            data['thumbnail'] = url

        return data
