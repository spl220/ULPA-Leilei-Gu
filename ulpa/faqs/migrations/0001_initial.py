# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FAQ',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(help_text=b'The date and time at which the object was entered into the system', verbose_name=b'Date created', auto_now_add=True)),
                ('modified', models.DateTimeField(help_text=b'The date and time at which the object was last modified', verbose_name=b'Date last modified', auto_now=True)),
                ('question', models.CharField(max_length=256)),
                ('answer', models.TextField()),
            ],
            options={
                'verbose_name': 'FAQ',
                'verbose_name_plural': 'FAQs',
            },
        ),
        migrations.CreateModel(
            name='FAQCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(help_text=b'The date and time at which the object was entered into the system', verbose_name=b'Date created', auto_now_add=True)),
                ('modified', models.DateTimeField(help_text=b'The date and time at which the object was last modified', verbose_name=b'Date last modified', auto_now=True)),
                ('name', models.CharField(max_length=256)),
            ],
            options={
                'verbose_name': 'FAQ category',
                'verbose_name_plural': 'FAQ categories',
            },
        ),
        migrations.AddField(
            model_name='faq',
            name='faq_category',
            field=models.ForeignKey(related_name='faqs', to='faqs.FAQCategory'),
        ),
    ]
