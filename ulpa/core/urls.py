# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import url

from . import views

urlpatterns = [
    # URL pattern for home
    url(r'^$', views.home, name='home'),
    url(r'^setup/$', views.setup, name="setup"),
    url(r'^force_500/$', views.force_500, name="force_500"),
    url(r'^health_check/$', views.health_check, name='health_check'),
    url(r'^about/$', views.about, name="about"),
    url(r'^contact/$', views.contact, name="contact"),
    url(r'^what-languages-can-i-study/$', views.what_languages_can_i_study,
        name="what-languages-can-i-study"),
    url(r'^why-study-languages/$', views.why_study_languages,
        name="why-study-languages"),
    url(r'^can-study-at-university-other-than-own/$', views.can_study_at_uni_other_than_own,
        name="can-study-at-university-other-than-own"),
    url(r'^where-can-study-indigenous-languages/$', views.where_can_study_indigenous_languages,
        name="where-can-study-indigenous-languages"),
    url(r'^google0181146fe649f777/$', views.google_verification, name="google0181146fe649f777"),
    url(r'^url-check/$', views.url_check, name="url-check"),
    url(r'^url-check-results/$', views.url_check_results, name="url-check-results"),
    url(r'^sitemap/$', views.sitemap, name="sitemap"),
]
