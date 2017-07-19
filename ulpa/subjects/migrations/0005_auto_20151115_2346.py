# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import select_multiple_field.models


class Migration(migrations.Migration):

    dependencies = [
        ('subjects', '0004_auto_20151115_2252'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subject',
            name='state',
            field=select_multiple_field.models.SelectMultipleField(max_length=256, choices=[('VIC', 'Victoria'), ('NSW', 'New South Wales'), ('SA', 'South Australia'), ('QLD', 'Queensland'), ('WA', 'Western Australia'), ('TAS', 'Tasmania'), ('ACT', 'Australian Capital Territory'), ('NT', 'Northern Territory')]),
        ),
        migrations.AlterField(
            model_name='subject',
            name='study_choice',
            field=models.CharField(max_length=256, choices=[('on-campus', "I want to study on-campus (but don't mind if a small portion is online)"), ('online', 'I want to study entirely online')]),
        ),
    ]
