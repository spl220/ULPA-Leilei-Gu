# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20150908_1358'),
    ]

    operations = [
        migrations.AlterField(
            model_name='siteconfiguration',
            name='copyright_statement',
            field=models.TextField(help_text=b'The site copyright statement, displayed in the footer', max_length=50, null=True, blank=True),
        ),
    ]
