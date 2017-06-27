# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^bulk_upload/(?P<bulk_upload_id>\d+)/confirm/', views.universities_confirm_bulk_upload, name='universities-confirm-bulk-upload'),
    url(r'^bulk_upload/', views.universities_bulk_upload, name='universities-bulk-upload'),
    url(r'^search/', views.university_search, name='university-search'),
    url(r'^list_languages/', views.list_languages, name='list-languages'),
]
