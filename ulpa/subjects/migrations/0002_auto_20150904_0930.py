# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import select_multiple_field.models


class Migration(migrations.Migration):

    dependencies = [
        ('subjects', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subject',
            name='intensity',
            field=select_multiple_field.models.SelectMultipleField(max_length=50, choices=[('Intensive', 'Intensive'), ('Regular', 'Regular/Non-intensive')]),
        ),
    ]
