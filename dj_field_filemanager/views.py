import mimetypes
import os
import stat

from django.apps import apps
from django.conf import settings
from django.http import (Http404, HttpResponse, HttpResponseForbidden,
                         HttpResponseNotModified)
from django.shortcuts import get_object_or_404
from django.utils.http import http_date
from django.views.static import was_modified_since


def _media_files_server(request, path):
    fullpath = os.path.join(settings.MEDIA_ROOT, path)
    if not os.path.exists(fullpath) or \
            not os.path.realpath(fullpath).startswith(settings.MEDIA_ROOT):
        raise Http404('"{0}" does not exist'.format(path))
    # Respect the If-Modified-Since header.
    statobj = os.stat(fullpath)
    content_type = mimetypes.guess_type(
        fullpath)[0] or 'application/octet-stream'
    if not was_modified_since(request.META.get('HTTP_IF_MODIFIED_SINCE'),
                              statobj[stat.ST_MTIME]):
        return HttpResponseNotModified(content_type=content_type)
    # FIXME: use FileResponse instead https://docs.djangoproject.com/en/3.0/ref/request-response/
    response = HttpResponse(
        open(fullpath, 'rb').read(), content_type=content_type)
    response["Last-Modified"] = http_date(statobj[stat.ST_MTIME])
    # filename = os.path.basename(path)
    # response['Content-Disposition'] = smart_str(u'attachment; filename={0}'.format(filename))
    return response


def filemanager_model_server(request, label, model, parent_pk, field, file, thumbnail):
    Model = apps.get_model(label, model)
    _ = get_object_or_404(Model, pk=parent_pk)
    if not request.user.is_authenticated or not request.user.has_perm('%s.view_%s' % (label, model)):
        return HttpResponseForbidden()
    folder = 'filemanager'
    if thumbnail:
        folder = '%s_thumbnails' % folder
    path = '%s/%s/%s/%s/%s/%s' % (label, model, parent_pk, field, folder, file)
    return _media_files_server(request, path)


def filemanager_storage_server(request, storage_code, file, thumbnail):
    print('storage_code', storage_code)
    print('file', file)
    storage_config = None
    for item in settings.FIELD_FILEMANAGER_STORAGE_CONFIG:
        if item['code'] == storage_code:
            storage_config = item
            break
    if not storage_config:
        raise Http404()
    if 'auth' in storage_config and storage_config['auth'] and  \
            (not request.user.is_authenticated or not request.user.has_perm('%s.view_%s' % (label, model))):
        return HttpResponseForbidden()

    if not thumbnail:
        path = os.path.join(storage_config['path'], file)
    else:
        path = os.path.join(storage_config['thumbnail']['path'], file)

    return _media_files_server(request, path)
