# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_siteconfiguration_copyright_statement'),
    ]

    operations = [
        migrations.RenameField(
            model_name='siteconfiguration',
            old_name='other_univeristy_content',
            new_name='other_university_content',
        ),
        migrations.RenameField(
            model_name='siteconfiguration',
            old_name='other_univeristy_heading',
            new_name='other_university_heading',
        ),
    ]
