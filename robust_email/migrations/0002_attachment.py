# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('robust_email', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attachment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content', models.FileField(null=True, upload_to=b'email_attachments', blank=True)),
                ('mimetype', models.CharField(help_text=b'e.g. text/html', max_length=255)),
                ('email', models.ForeignKey(to='robust_email.EmailMessage')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
