from django.conf import settings

from .models import SiteConfiguration


def site_configuration(request):
    available_configurations = SiteConfiguration.objects.all()

    if 'site_configuration' in request.session:
        site_configuration_id = request.session['site_configuration']

        try:
            site_configuration = SiteConfiguration.objects.get(pk=site_configuration_id)

            return {
                'site_configuration': site_configuration,
                'available_configurations': available_configurations,
            }

        except SiteConfiguration.DoesNotExist:
            pass

    site_configuration = SiteConfiguration.objects.get_current()

    return {
        'site_configuration': site_configuration,
        'available_configurations': available_configurations,
    }

def global_settings(request):
    return {
        'GOOGLE_ANALYTICS': settings.GOOGLE_ANALYTICS,
        'GOOGLE_API_KEY': settings.GOOGLE_API_KEY
    }