# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='University',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(help_text=b'The date and time at which the object was entered into the system', verbose_name=b'Date created', auto_now_add=True)),
                ('modified', models.DateTimeField(help_text=b'The date and time at which the object was last modified', verbose_name=b'Date last modified', auto_now=True)),
                ('name', models.CharField(max_length=256)),
                ('url', models.URLField(blank=True)),
                ('cross_institutional_url', models.URLField(blank=True)),
                ('logo', models.ImageField(help_text='Max size: 120px x 40px', upload_to=b'', blank=True)),
            ],
            options={
                'ordering': ('name',),
                'verbose_name': 'university',
                'verbose_name_plural': 'universities',
            },
        ),
        migrations.CreateModel(
            name='UniversityBulkUpload',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(help_text=b'The date and time at which the object was entered into the system', verbose_name=b'Date created', auto_now_add=True)),
                ('modified', models.DateTimeField(help_text=b'The date and time at which the object was last modified', verbose_name=b'Date last modified', auto_now=True)),
                ('status', models.CharField(default='pending', max_length=50, choices=[('pending', 'Pending'), ('processed', 'Processed'), ('cancelled', 'Cancelled')])),
                ('xlsx_file', models.FileField(upload_to='university_bulk_uploads')),
                ('user', models.ForeignKey(related_name='university_bulk_uploads', on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
