# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='siteconfiguration',
            name='copyright_statement',
            field=models.TextField(help_text=b'The site copyright statement, displayed in the footer', null=True, blank=True),
        ),
    ]
