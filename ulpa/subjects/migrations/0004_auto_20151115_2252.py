# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import select_multiple_field.models


class Migration(migrations.Migration):

    dependencies = [
        ('subjects', '0003_auto_20150909_1300'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subject',
            name='intensity',
            field=select_multiple_field.models.SelectMultipleField(max_length=50, choices=[('intensive', 'I want to do an intensive course (eg. summer school)'), ('regular', 'I want to study over a regular semester')]),
        ),
        migrations.AlterField(
            model_name='subject',
            name='study_choice',
            field=models.CharField(max_length=256, choices=[('on-campus', "I want to study on-campus (but don't mind if a small portion is online)"), ('online', 'I want to study entirely online'), ('both', 'Both')]),
        ),
    ]
