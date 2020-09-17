from django.conf.urls import include
from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('dj_field_filemanager/', include('dj_field_filemanager.urls')),
    path('upload_to_folder/', TemplateView.as_view(template_name="upload_to_folder.html"),
         name='upload_to_folder_example'),
]
