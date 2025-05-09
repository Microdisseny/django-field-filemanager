# Generated by Django 2.1.15 on 2025-04-25 10:55

import dj_field_filemanager.models
import dj_field_filemanager.storage
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, verbose_name='Name')),
                ('file', models.FileField(max_length=255, storage=dj_field_filemanager.storage.OverwriteStorage(), upload_to=dj_field_filemanager.models._upload_to, verbose_name='File')),
                ('thumbnail', models.FileField(blank=True, max_length=255, null=True, storage=dj_field_filemanager.storage.OverwriteStorage(), upload_to=dj_field_filemanager.models._thumbnail_upload_to, verbose_name='Thumbnail')),
                ('folder', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='documents.Folder')),
            ],
            bases=(dj_field_filemanager.models.ThumbnailMixin, models.Model),
        ),
        migrations.AlterUniqueTogether(
            name='image',
            unique_together={('name', 'folder')},
        ),
    ]
