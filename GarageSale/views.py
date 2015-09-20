import sys
import requests
import postmates
import httplib
import json
import urllib

from django.core.exceptions import PermissionDenied
from django.http import (HttpResponse, HttpResponseNotFound,
    HttpResponseBadRequest, HttpResponseServerError)
from django.views.generic.base import View
from django.views.generic import TemplateView
from django.shortcuts import render
from django.contrib.auth.views import redirect_to_login

from GarageSale.forms import DeliveryQuoteForm

import json,httplib, urllib



class ErrorView(View):
    """ HTTP 500: Internal Server Error """
    template_name = '500.html'
    status = 500
    
    def get(self, request):
        return render(request, self.template_name, status=self.status)
    
    
class PermissionDeniedView(ErrorView):
    """ HTTP 403: Forbidden """
    template_name = '403.html'
    status = 403
    
    
class NotFoundView(ErrorView):
    """ HTTP 404: Not Found """
    template_name = '404.html'
    status = 404
    
    
class IndexPage(TemplateView):

    def get(self, request):
        params = request.GET
        connection = httplib.HTTPSConnection('api.parse.com', 443)
        constraints = {
           "username": {
                "$ne": "bob"
            }
         }
        if 'keyword' in params:
            constraints["name"] = {
                "$in": params['location']
            }


        search_params = urllib.urlencode({"where":json.dumps(constraints)})
        connection.connect()
        connection.request('GET', '/1/classes/Items?%s' % search_params, '', {
               "X-Parse-Application-Id": "GEhB6O9S9sJwKWRVlfcm2zghfmpN7ZIg5guhjHha",
               "X-Parse-REST-API-Key": "Ui7OtToUquSRwLGGHxDCLB0nX9t5o2IOwSVyRjRI"
             })
        result = json.loads(connection.getresponse().read())
        items = result['results']
        return render(request, 'index.html', {"items": items, "locations": json.dumps(items)})

class LoginPage(TemplateView):
    """ The Account Page. """
    template_name = 'Login.html'

class GaragePage(TemplateView):
    """ The Garage Page. """
    #template_name = 'garage.html'
    def get(self, request):
       connection = httplib.HTTPSConnection('api.parse.com', 443)
       params1 = urllib.urlencode({"where":json.dumps({
          "username": "bob",
          "status" : "IN TRANSIT"
          })})
       params2 = urllib.urlencode({"where":json.dumps({
          "username": "bob",
          "status" : "UNSOLD"
          })})
       params3 = urllib.urlencode({"where":json.dumps({
          "username": "bob",
          "status" : "SOLD"
          })})
       connection.connect()
       connection.request('GET', '/1/classes/Items?%s' % params1, '', {
              "X-Parse-Application-Id": "GEhB6O9S9sJwKWRVlfcm2zghfmpN7ZIg5guhjHha",
              "X-Parse-REST-API-Key": "Ui7OtToUquSRwLGGHxDCLB0nX9t5o2IOwSVyRjRI"
            })
       result = json.loads(connection.getresponse().read())
       trans_items = result['results']
       connection.request('GET', '/1/classes/Items?%s' % params2, '', {
              "X-Parse-Application-Id": "GEhB6O9S9sJwKWRVlfcm2zghfmpN7ZIg5guhjHha",
              "X-Parse-REST-API-Key": "Ui7OtToUquSRwLGGHxDCLB0nX9t5o2IOwSVyRjRI"
            })
       result = json.loads(connection.getresponse().read())
       unsold_items = result['results']
       connection.request('GET', '/1/classes/Items?%s' % params3, '', {
              "X-Parse-Application-Id": "GEhB6O9S9sJwKWRVlfcm2zghfmpN7ZIg5guhjHha",
              "X-Parse-REST-API-Key": "Ui7OtToUquSRwLGGHxDCLB0nX9t5o2IOwSVyRjRI"
            })
       result = json.loads(connection.getresponse().read())
       sold_items = result['results']
       return render(request, 'garage.html', {"trans_items": trans_items, "unsold_items" : unsold_items,
                                              "sold_items" : sold_items})

class OrdersPage(TemplateView):
    """ The Orders Page. """
    template_name = 'orders.html'

class AccountPage(TemplateView):
    """ The Account Page. """
    template_name = 'account.html'
    
    
def staff_only(view):
    """ Staff-only View decorator. """
    
    def decorated_view(request, *args, **kwargs):
        if not request.user.is_authenticated():
            return redirect_to_login(request.get_full_path())
            
        if not request.user.is_staff:
            raise PermissionDenied
            
        return view(request, *args, **kwargs)
        
    return decorated_view
    
    

