# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^bulk_upload/(?P<bulk_upload_id>\d+)/confirm/', views.languages_confirm_bulk_upload, name='languages-confirm-bulk-upload'),
    url(r'^bulk_upload/', views.languages_bulk_upload, name='languages-bulk-upload'),
    url(r'^search/', views.language_search, name='language-search'),
    url(r'^individual/(?P<language>[-\w]+)$', views.individual_language, name='individual-language'),
    url(r'^category/(?P<category>[-\w]+)$', views.category_language, name='category-language'),
    url(r'^list_universities/', views.list_universities, name='list-universities'),
    url(r'^list_potential_subjects/', views.list_potential_subjects, name='list-potential-subjects'),
]
