# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SiteConfiguration',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(help_text=b'The date and time at which the object was entered into the system', verbose_name=b'Date created', auto_now_add=True)),
                ('modified', models.DateTimeField(help_text=b'The date and time at which the object was last modified', verbose_name=b'Date last modified', auto_now=True)),
                ('active', models.BooleanField(default=False, help_text=b'If ticked, the settings in this configuration will become live.')),
                ('name', models.CharField(help_text=b'A name for this collection. For reference only.', max_length=255)),
                ('creative_commons_statement', models.TextField(help_text=b'The site creative commons notice, displayed in the footer', null=True, blank=True)),
                ('liability_statement', models.TextField(help_text=b'The site liability notice, displayed in the footer', null=True, blank=True)),
                ('privacy_policy', models.TextField(help_text=b'The site privacy policy, displayed in the footer', null=True, blank=True)),
                ('disclaimer_statement', models.TextField(help_text=b'The site disclaimer notice, displayed in the footer', null=True, blank=True)),
                ('terms_of_use_statement', models.TextField(help_text=b'The site terms of use, displayed in the footer', null=True, blank=True)),
                ('page_not_found_content', models.TextField(help_text=b'The copy text that appears on the 404 page', null=True, blank=True)),
                ('home_page_heading', models.CharField(help_text=b'The heading that appears above the textual content on the home page', max_length=255, null=True, blank=True)),
                ('home_page_content', models.TextField(help_text=b'The textual content that appears at the top of the home page', null=True, blank=True)),
                ('about_page_heading', models.CharField(help_text=b'The heading that appears above the textual content on the about page', max_length=255, null=True, blank=True)),
                ('about_page_content', models.TextField(help_text=b'The textual content that appears at the top of the about page', null=True, blank=True)),
                ('other_univeristy_heading', models.CharField(help_text=b'The heading that appears above the textual content on the resources page', max_length=255, null=True, blank=True)),
                ('other_univeristy_content', models.TextField(help_text=b'The textual content that appears at the top of the resources page', null=True, blank=True)),
                ('where_can_study_indigenous_languages_heading', models.CharField(help_text=b'The heading that appears above the textual content on the register interest page', max_length=255, null=True, blank=True)),
                ('where_can_study_indigenous_languages_content', models.TextField(help_text=b'The textual content that appears at the top of the register interest page', null=True, blank=True)),
                ('what_languages_can_study_heading', models.CharField(help_text=b'The heading that appears above the textual content on the register interest page', max_length=255, null=True, blank=True)),
                ('what_languages_can_study_content', models.TextField(help_text=b'The textual content that appears at the top of the register interest page', null=True, blank=True)),
                ('why_study_languages_heading', models.CharField(help_text=b'The heading that appears above the textual content on the register interest page', max_length=255, null=True, blank=True)),
                ('why_study_languages_content', models.TextField(help_text=b'The textual content that appears at the top of the register interest page', null=True, blank=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
    ]
