import os

from django.contrib import admin

from dj_field_filemanager.admin import FieldFilemanagerAdmin

from .models import Document, Folder, Image, Project


class FolderInline(FieldFilemanagerAdmin, admin.StackedInline):
    model = Folder
    extra = 0
    fields = ('id', 'name',)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    """
    Admin for manage Project
    """
    list_display = ('id', 'name',)
    list_display_links = ('id', 'name',)
    inlines = [FolderInline]


@admin.register(Folder)
class FolderAdmin(FieldFilemanagerAdmin, admin.ModelAdmin):
    """
    Admin for manage folders
    """
    list_display = ('id', 'name',)
    list_display_links = ('id', 'name',)
    document_display_modes = {
        'documents.Document': 'list',
        'documents.Image': 'grid',
    }


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    """
    Admin for manage documents
    """
    list_display = ('id', 'name',)
    list_display_links = ('id', 'name',)

    def save_model(self, request, obj, form, change):
        if not obj.name:
            obj.name = os.path.basename(obj.file.name)
        super().save_model(request, obj, form, change)
        obj.save_thumbnail()


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    """
    Admin to manage images
    """

    list_display = (
        "id",
        "name",
    )
    list_display_links = (
        "id",
        "name",
    )

    def save_model(self, request, obj, form, change):
        if not obj.name:
            obj.name = os.path.basename(obj.file.name)
        super().save_model(request, obj, form, change)
        obj.save_thumbnail()
