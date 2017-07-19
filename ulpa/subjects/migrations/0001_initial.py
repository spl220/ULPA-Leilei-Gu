# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
import select_multiple_field.models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('languages', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('universities', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(help_text=b'The date and time at which the object was entered into the system', verbose_name=b'Date created', auto_now_add=True)),
                ('modified', models.DateTimeField(help_text=b'The date and time at which the object was last modified', verbose_name=b'Date last modified', auto_now=True)),
                ('title', models.CharField(max_length=256)),
                ('code', models.CharField(max_length=256)),
                ('url', models.URLField(blank=True)),
                ('state', models.CharField(max_length=256, choices=[('VIC', 'Victoria'), ('NSW', 'New South Wales'), ('SA', 'South Australia'), ('QLD', 'Queensland'), ('WA', 'Western Australia'), ('TAS', 'Tasmania'), ('ACT', 'Australian Capital Territory'), ('NT', 'Northern Territory')])),
                ('other_university', models.TextField(max_length=512, null=True, blank=True)),
                ('intensity', select_multiple_field.models.SelectMultipleField(max_length=3, choices=[('I', 'Intensive'), ('R', 'Regular/Non-intensive')])),
                ('prerequisite', models.TextField(max_length=512, null=True, blank=True)),
                ('non_beginner_level_available', models.BooleanField(default=False)),
                ('next_offered', models.TextField(null=True, blank=True)),
                ('study_choice', models.CharField(max_length=256, choices=[('on-campus', 'On campus (may be partially online)'), ('online', 'Fully-online')])),
                ('notes', models.TextField(blank=True)),
                ('language', models.ForeignKey(related_name='subjects', to='languages.Language', max_length=256)),
                ('university', models.ForeignKey(related_name='subjects', to='universities.University', max_length=256)),
            ],
            options={
                'ordering': ['language', 'title'],
                'verbose_name': 'subject',
                'verbose_name_plural': 'subjects',
            },
        ),
        migrations.CreateModel(
            name='SubjectBulkUpload',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(help_text=b'The date and time at which the object was entered into the system', verbose_name=b'Date created', auto_now_add=True)),
                ('modified', models.DateTimeField(help_text=b'The date and time at which the object was last modified', verbose_name=b'Date last modified', auto_now=True)),
                ('status', models.CharField(default='pending', max_length=50, choices=[('pending', 'Pending'), ('processed', 'Processed'), ('cancelled', 'Cancelled')])),
                ('xlsx_file', models.FileField(upload_to='subject_bulk_uploads')),
                ('user', models.ForeignKey(related_name='subject_bulk_uploads', on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
