

class SiteConfigurationMiddleware(object):
    def process_request(self, request):
        if 'site_configuration' in request.GET:
            request.session['site_configuration'] = request.GET['site_configuration']
