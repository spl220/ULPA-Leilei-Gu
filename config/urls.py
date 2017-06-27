# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin

urlpatterns = [
    # Django Admin
    url(r'^admin/', include(admin.site.urls)),

    # Core urls
    url(r'^', include("ulpa.core.urls", namespace="core")),

    # User management
    url(r'^users/', include("ulpa.users.urls", namespace="users")),

    # Language urls
    url(r'^languages/', include("ulpa.languages.urls", namespace="languages")),

    # Subject urls
    url(r'^subjects/', include("ulpa.subjects.urls", namespace="subjects")),

    # University urls
    url(r'^universities/', include("ulpa.universities.urls", namespace="universities")),

    # FAQ url
    url(r'^faqs/', include("ulpa.faqs.urls", namespace="faqs")),

    # Robust Email
    url(r'^email/', include("robust_email.urls")),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        url(r'^400/$', 'django.views.defaults.bad_request'),
        url(r'^403/$', 'django.views.defaults.permission_denied'),
        url(r'^404/$', 'django.views.defaults.page_not_found'),
        url(r'^500/$', 'django.views.defaults.server_error'),
    ]
