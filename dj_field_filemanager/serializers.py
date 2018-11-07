from rest_framework.serializers import ModelSerializer


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
