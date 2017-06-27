# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import select_multiple_field.models


class Migration(migrations.Migration):

    dependencies = [
        ('subjects', '0002_auto_20150904_0930'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subject',
            name='intensity',
            field=select_multiple_field.models.SelectMultipleField(max_length=50, choices=[('intensive', 'Intensive'), ('regular', 'Regular/Non-intensive')]),
        ),
    ]
