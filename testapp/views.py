from django.http import HttpResponse
from django.views.generic.base import View
from django.core.exceptions import PermissionDenied


class EchoView(View):
    """ Test View for echoing GET and POST request data. """
    
    def get(self, request):
        response = '\n'.join(
                ('='.join(pair) for pair in request.GET.iteritems())
            )
        return HttpResponse(response)
        
    def post(self, request):
        response = '\n'.join(
                ('='.join(pair) for pair in request.POST.iteritems())
            )
        return HttpResponse(response)
        
        
class Generate403View(View):
    """ Test View for generating an HTTP 403. """
    
    def get(self, request):
        raise PermissionDenied
        
        
class Generate500View(View):
    """ Test View for generating an HTTP 500. """
    
    def get(self, request):
        raise Exception("Generated Test Exception")
        
        