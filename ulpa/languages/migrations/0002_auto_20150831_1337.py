# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('languages', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='language',
            name='slug',
            field=models.SlugField(default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='languagecategory',
            name='slug',
            field=models.SlugField(default=''),
            preserve_default=False,
        ),
    ]
