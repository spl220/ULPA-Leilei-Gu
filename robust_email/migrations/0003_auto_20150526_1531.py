# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('robust_email', '0002_attachment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailmessage',
            name='from_email',
            field=models.EmailField(max_length=254, blank=True),
        ),
    ]
