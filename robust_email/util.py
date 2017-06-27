from hashlib import sha1 as sha_constructor

from django.utils.html import strip_tags
from django.conf import settings
import re

HREF_RE = re.compile(
    r'<a[^>+]href\s*=\s*["\'](?P<href>[^>\'"]*)["\'].*>(?P<text>.*)</a>',
    re.IGNORECASE)

def replace_link(match):
    return '%(text)s (%(href)s)' % match.groupdict()

def html_to_text(html):
    """ Try to convert HTML message to user-friendly text-only version.

    Just using strip_tags or similar will mean that:
        <a href="http://...">Click here</a> to unsubscribe.
    becomes:
        Click here to unsubscribe.
    for example, leaving readers rather unhappy.
    """
    html = HREF_RE.sub(replace_link, html)
    return strip_tags(html)

def exception_class_string(exception_class):
    return "%s.%s" % (exception_class.__module__, exception_class.__name__)

def get_token(obj, text=''):
    return sha_constructor(
        settings.SECRET_KEY + unicode(obj.id) + text).hexdigest()[::3]