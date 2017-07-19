# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import *

from . import views

MESSAGE_ID_PATTERN = r'(?P<message_id>\d+)a(?P<token>.+)'

urlpatterns = [
    url(r'view/%s/$' % MESSAGE_ID_PATTERN, views.view_email, name='view_email'),
    ]