# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings
import robust_email.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AlternativeContent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content', models.TextField(blank=True)),
                ('mimetype', models.CharField(help_text=b'e.g. text/html', max_length=255)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EmailMessage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('to', robust_email.fields.EmailListField(help_text=b'Comma-separated list of email addresses', blank=True)),
                ('from_email', models.EmailField(max_length=75, blank=True)),
                ('bcc', robust_email.fields.EmailListField(help_text=b'Comma-separated list of email addresses', blank=True)),
                ('subject', models.TextField(blank=True)),
                ('body', models.TextField(blank=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(related_name=b'email_messages', on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ['-created'],
                'get_latest_by': 'created',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EmailTransaction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('exception_type', models.CharField(max_length=255, blank=True)),
                ('exception_value', models.CharField(max_length=1024, blank=True)),
                ('when', models.DateTimeField(auto_now_add=True)),
                ('email', models.ForeignKey(to='robust_email.EmailMessage')),
            ],
            options={
                'ordering': ['-when'],
                'get_latest_by': 'when',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='alternativecontent',
            name='email',
            field=models.ForeignKey(to='robust_email.EmailMessage'),
            preserve_default=True,
        ),
    ]
