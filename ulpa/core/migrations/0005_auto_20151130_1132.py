# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20150909_1300'),
    ]

    operations = [
        migrations.AddField(
            model_name='siteconfiguration',
            name='facebook_description',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='siteconfiguration',
            name='facebook_image',
            field=models.ImageField(null=True, upload_to=b'', blank=True),
        ),
        migrations.AddField(
            model_name='siteconfiguration',
            name='facebook_title',
            field=models.CharField(max_length=256, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='siteconfiguration',
            name='facebook_url',
            field=models.URLField(null=True, blank=True),
        ),
    ]
