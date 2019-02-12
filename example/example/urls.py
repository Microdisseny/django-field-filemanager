"""example URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin

try:
    from django.urls import include
except ImportError:  # Django<2.0
    from django.conf.urls import include

try:
    from django.urls import re_path
except ImportError:  # Django<2.0
    from django.conf.urls import url as re_path

from django.views.generic import TemplateView

urlpatterns = [
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^dj_field_filemanager/', include('dj_field_filemanager.urls')),
    re_path(r'^upload_to_folder/', TemplateView.as_view(template_name="upload_to_folder.html"),
            name='upload_to_folder_example'),
]

urlpatterns += static('media', document_root=settings.MEDIA_ROOT)
