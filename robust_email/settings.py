from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from importlib import import_module
import sys



def prefixed(string):
    return 'ROBUST_EMAIL_%s' % string

SETTINGS = {
    'VIEW_EMAIL_ONLINE_URL_PLACEHOLDER':
        prefixed('VIEW_EMAIL_ONLINE_URL_PLACEHOLDER'),
    'DKIM_ON': False,
    }


backend = getattr(settings, "EMAIL_BACKEND", None)
celery_backend = getattr(settings, "CELERY_EMAIL_BACKEND", None)


if celery_backend and 'CeleryEmailBackend' in backend:
    backend = celery_backend


# If they're using our backend..
if 'robust_email' in backend:
    # Grab the path of the 'base' email backend
    path = getattr(settings, "BASE_EMAIL_BACKEND", None)

    # If they haven't defined a base backend, raise an error
    if not path:
        raise ImproperlyConfigured(("Must define BASE_EMAIL_BACKEND if using robust_email.backends.DatabaseBackend"))

    # Try to locate the module
    try:
        mod_name, klass_name = path.rsplit('.', 1)
        mod = import_module(mod_name)
    except ImportError as e:
        raise ImproperlyConfigured(('Error importing email backend module %s: "%s"'
                                    % (mod_name, e)))

    # Try to locate the class within the module
    try:
        klass = getattr(mod, klass_name)
    except AttributeError:
        raise ImproperlyConfigured(('Module "%s" does not define a '
                                    '"%s" class' % (mod_name, klass_name)))

    # Set the class in our local settings dict
    SETTINGS['BASE_EMAIL_BACKEND'] = klass


# Turn the settings dictionary into an object
for name, default in SETTINGS.items():
    setattr(sys.modules[__name__], name,
            getattr(settings, prefixed(name), default))
