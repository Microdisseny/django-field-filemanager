from django.db import models

from dj_field_filemanager.models import DocumentModel


class Project(models.Model):
    name = models.CharField(max_length=50)


class Folder(models.Model):
    project = models.ForeignKey(Project, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Document(DocumentModel):
    document_parent = 'folder'
    folder = models.ForeignKey(Folder, null=False, blank=False, on_delete=models.CASCADE)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        unique_together = (('name', 'folder'),)


class Image(DocumentModel):
    document_parent = "folder"
    folder = models.ForeignKey(
        Folder, null=False, blank=False, on_delete=models.CASCADE
    )
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        unique_together = (("name", "folder"),)
