# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^bulk_upload/(?P<bulk_upload_id>\d+)/confirm/', views.subjects_confirm_bulk_upload, name='subjects-confirm-bulk-upload'),
    url(r'^bulk_upload/', views.subjects_bulk_upload, name='subjects-bulk-upload'),
    url(r'^search_results/', views.subject_search_results, name='subject-search-results'),
    url(r'^printable_search_results/', views.printable_subject_search_results, name='printable-subject-search-results'),
]
