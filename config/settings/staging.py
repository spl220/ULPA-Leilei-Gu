# -*- coding: utf-8 -*-
'''
Staging Server Configuration

- Use Amazon's S3 for storing uploaded media
'''
from __future__ import absolute_import, unicode_literals


from boto.s3.connection import OrdinaryCallingFormat
from django.utils import six

from .common import *  # noqa

# GOOGLE ANALYTICS
GOOGLE_ANALYTICS = "UA-67132878-3"
GOOGLE_API_KEY = ""


# SECRET CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
# Raises ImproperlyConfigured exception if DJANO_SECRET_KEY not in os.environ
SECRET_KEY = env("DJANGO_SECRET_KEY")


# SITE CONFIGURATION
# ------------------------------------------------------------------------------
# Hosts/domain names that are valid for this site
# See https://docs.djangoproject.com/en/1.6/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ["ulpa.wspdigitalstaging.com",]
# END SITE CONFIGURATION


# STORAGE CONFIGURATION
# ------------------------------------------------------------------------------
# Uploaded Media Files
# ------------------------
# See: http://django-storages.readthedocs.org/en/latest/index.html
INSTALLED_APPS += (
    'storages',
    # 'lockdown'
)
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'

AWS_STORAGE_BUCKET_NAME = env('DJANGO_AWS_STORAGE_BUCKET_NAME')
AWS_AUTO_CREATE_BUCKET = False
AWS_QUERYSTRING_AUTH = False
AWS_S3_SECURE_URLS = False
AWS_S3_HOST = 's3-ap-southeast-2.amazonaws.com'
AWS_S3_CALLING_FORMAT = OrdinaryCallingFormat()
# AWS_SES_REGION_NAME = 'us-west-2'
# AWS_SES_REGION_ENDPOINT = 'email.us-west-2.amazonaws.com'

# Bypasses S3's URL parameter authentication stuff
AWS_S3_CUSTOM_DOMAIN = 'media-ulpa-wspdigitalstaging-com.s3.amazonaws.com'

# AWS cache settings, don't change unless you know what you're doing:
AWS_EXPIRY = 60 * 60 * 24 * 7

# TODO See: https://github.com/jschneier/django-storages/issues/47
# Revert the following and use str after the above-mentioned bug is fixed in
# either django-storage-redux or boto
AWS_HEADERS = {
    'Cache-Control': six.b('max-age=%d, s-maxage=%d, must-revalidate' % (
        AWS_EXPIRY, AWS_EXPIRY))
}

# URL that handles the media served from MEDIA_ROOT, used for managing stored files.
MEDIA_URL = 'https://s3.amazonaws.com/%s/' % AWS_STORAGE_BUCKET_NAME


# EMAIL
# ------------------------------------------------------------------------------
EMAIL_BACKEND = 'robust_email.backends.DatabaseBackend'
BASE_EMAIL_BACKEND = 'django_ses.SESBackend'
SERVER_EMAIL = 'noreply@wspdigital.com'
DEFAULT_FROM_EMAIL = 'noreply@wspdigital.com'
EMAIL_RECIPIENTS = ['infrastructure@wspdigital.com']
AWS_SES_ACCESS_KEY_ID = env('DJANGO_AWS_SES_ACCESS_KEY_ID')
AWS_SES_SECRET_ACCESS_KEY = env('DJANGO_AWS_SES_SECRET_ACCESS_KEY')


# TEMPLATE CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#template-dirs
TEMPLATE_LOADERS = (
    ('django.template.loaders.cached.Loader', (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    )),
)


# DATABASE CONFIGURATION
# ------------------------------------------------------------------------------
# Raises ImproperlyConfigured exception if DATABASE_URL not in os.environ
DATABASES['default'] = env.db("DATABASE_URL")


# CACHING
# ------------------------------------------------------------------------------
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'ddr'
    },
    'locations': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'locations-cache',
        'TIMEOUT': 22896000,  # 1 Year
        'OPTIONS': {
            'MAX_ENTRIES': 10000,
        },
    }
}

# LOCKDOWN PASSWORD
# -------------------------------------------------------------------------------
# LOCKDOWN_PASSWORDS = ('5HQMdh3A')

# MIDDLEWARE
# ------------------------------------------------------------------------------
MIDDLEWARE_CLASSES += (
    # 'lockdown.middleware.LockdownMiddleware',
)

# Error logging
# ------------------------------------------------------------------------------

RAVEN_CONFIG = {
    'dsn': 'https://23ea8bd7cca441e8b2f58516b9bd64d7:5a6f6eab41cc48239ba01dc67348c4ee@app.getsentry.com/47533',
}


INSTALLED_APPS = INSTALLED_APPS + (
    'raven.contrib.django.raven_compat',
)
