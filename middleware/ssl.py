from django.conf import settings
from django.http import HttpResponseRedirect


class SSLMiddleware(object):
    def process_request(self, request):
        if not any((settings.DEBUG, settings.NO_SSL, request.is_secure())):
            url = request.build_absolute_uri(request.get_full_path())
            secure_url = url.replace('http://', 'https://')
            return HttpResponseRedirect(secure_url)
            
            