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
            name='Language',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(help_text=b'The date and time at which the object was entered into the system', verbose_name=b'Date created', auto_now_add=True)),
                ('modified', models.DateTimeField(help_text=b'The date and time at which the object was last modified', verbose_name=b'Date last modified', auto_now=True)),
                ('name', models.CharField(unique=True, max_length=256)),
                ('alternative_name', models.CharField(max_length=256, blank=True)),
                ('individual_language', models.TextField(max_length=512)),
                ('description', models.TextField()),
                ('how_widely_taught', models.CharField(max_length=256)),
                ('abs_data', models.TextField(max_length=512, null=True, blank=True)),
                ('abs_classification', models.CharField(max_length=256, null=True, blank=True)),
            ],
            options={
                'ordering': ('name',),
                'verbose_name': 'language',
                'verbose_name_plural': 'languages',
            },
        ),
        migrations.CreateModel(
            name='LanguageBulkUpload',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(help_text=b'The date and time at which the object was entered into the system', verbose_name=b'Date created', auto_now_add=True)),
                ('modified', models.DateTimeField(help_text=b'The date and time at which the object was last modified', verbose_name=b'Date last modified', auto_now=True)),
                ('status', models.CharField(default='pending', max_length=50, choices=[('pending', 'Pending'), ('processed', 'Processed'), ('cancelled', 'Cancelled')])),
                ('xlsx_file', models.FileField(upload_to='languages_bulk_uploads')),
                ('user', models.ForeignKey(related_name='language_bulk_uploads', on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='LanguageCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(help_text=b'The date and time at which the object was entered into the system', verbose_name=b'Date created', auto_now_add=True)),
                ('modified', models.DateTimeField(help_text=b'The date and time at which the object was last modified', verbose_name=b'Date last modified', auto_now=True)),
                ('name', models.CharField(unique=True, max_length=256, blank=True)),
                ('description', models.TextField(blank=True)),
            ],
            options={
                'verbose_name': 'language category',
                'verbose_name_plural': 'language categories',
            },
        ),
        migrations.AddField(
            model_name='language',
            name='categories',
            field=models.ManyToManyField(related_name='languages', to='languages.LanguageCategory', blank=True),
        ),
    ]
