import sys
import requests
import postmates
import httplib
import json
import urllib

from django.core.exceptions import PermissionDenied
from django.http import (HttpResponse, HttpResponseNotFound,
    HttpResponseBadRequest, HttpResponseServerError, HttpResponseRedirect)
from django.views.generic.base import View
from django.views.generic import TemplateView
from django.shortcuts import render
from django.contrib.auth.views import redirect_to_login

from GarageSale.forms import DeliveryQuoteForm

import json,httplib, urllib
import postmates as pm
import random
from django.templatetags.static import static



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
    """ The Index Page. """
    #template_name = 'index.html'
    def get(self, request):
        params = request.GET
        connection = httplib.HTTPSConnection('api.parse.com', 443)
        constraints = {
           "username": {
                "$ne": "bob"
            }
         }

        search_params = urllib.urlencode({"where":json.dumps(constraints)})
        connection.connect()
        connection.request('GET', '/1/classes/Items?%s' % search_params, '', {
               "X-Parse-Application-Id": "GEhB6O9S9sJwKWRVlfcm2zghfmpN7ZIg5guhjHha",
               "X-Parse-REST-API-Key": "Ui7OtToUquSRwLGGHxDCLB0nX9t5o2IOwSVyRjRI"
             })
        result = json.loads(connection.getresponse().read())
        items = result['results']
        json_items = json.dumps(items)
        # return HttpResponse(items)
        return render(request, 'index.html', {"items": items, "locations": json_items})

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


class MyCartPage(TemplateView):
    """ The Orders Page. """

    def common(self, request):
        test_key = '03c270d0-d388-4c1a-8aad-468de79ecfde'
        test_id = 'cus_KUuM-I53KYnm5F'
        api = pm.PostmatesAPI(test_key, test_id)


        connection = httplib.HTTPSConnection('api.parse.com', 443)
        params = urllib.urlencode({"where":json.dumps({
          "username": {"$ne" : "bob"},
          "status" : "IN TRANSIT"
          })})

        connection.connect()
        connection.request('GET', '/1/classes/Items?%s' % params, '', {
              "X-Parse-Application-Id": "GEhB6O9S9sJwKWRVlfcm2zghfmpN7ZIg5guhjHha",
              "X-Parse-REST-API-Key": "Ui7OtToUquSRwLGGHxDCLB0nX9t5o2IOwSVyRjRI"
            })
        result = json.loads(connection.getresponse().read())
        trans_items = result['results']

        item_costs = []
        total = 0 

        for item in trans_items:
            total += item["price"]
            pickup = pm.Location("source", '5520 Forbes Ave, Pittsburgh, PA', '415-555-0000')
            dropoff = pm.Location('bob', '5234 Forbes Ave, Pittsburgh, PA', '415-777-9999')
            quote = pm.DeliveryQuote(api, pickup.address, dropoff.address)
            cost = float(quote.fee)/100
            total += cost
            item_costs.append( [item, cost] )

        #return HttpResponse(str(cost) + " " +str(total))

        return render(request, 'mycart.html', {"item_costs" : item_costs, "total" : total})

    def get(self, request):
        return self.common(request)
        
    def post(self, request):
        get_params = request.POST
        if "item" in get_params:
            connection = httplib.HTTPSConnection('api.parse.com', 443)
            connection.connect()
            connection.request('PUT', '/1/classes/Items/' + get_params["item"], json.dumps({
                   "status": "IN TRANSIT"
                 }), {
                   "X-Parse-Application-Id": "GEhB6O9S9sJwKWRVlfcm2zghfmpN7ZIg5guhjHha",
                   "X-Parse-REST-API-Key": "Ui7OtToUquSRwLGGHxDCLB0nX9t5o2IOwSVyRjRI",
                   "Content-Type": "application/json"
                 })

        return self.common(request)

class OrdersPage(TemplateView):
    """ The Orders Page. """
    template_name = 'orders.html'
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
       return render(request, 'orders.html', {"trans_items": trans_items, "unsold_items" : unsold_items,
                                              "sold_items" : sold_items})


class CheckoutPage(TemplateView):
    """ The Account Page. """
    def post(self, request):
        test_key = '03c270d0-d388-4c1a-8aad-468de79ecfde'
        test_id = 'cus_KUuM-I53KYnm5F'
        api = pm.PostmatesAPI(test_key, test_id)


        connection = httplib.HTTPSConnection('api.parse.com', 443)
        params = urllib.urlencode({"where":json.dumps({
          "username": {"$ne" : "bob"},
          "status" : "IN TRANSIT"
          })})

        connection.connect()
        connection.request('GET', '/1/classes/Items?%s' % params, '', {
              "X-Parse-Application-Id": "GEhB6O9S9sJwKWRVlfcm2zghfmpN7ZIg5guhjHha",
              "X-Parse-REST-API-Key": "Ui7OtToUquSRwLGGHxDCLB0nX9t5o2IOwSVyRjRI"
            })
        result = json.loads(connection.getresponse().read())
        trans_items = result['results']

        for item in trans_items:
            pickup = pm.Location(item['username'], item['address'], '415-555-0000')
            dropoff = pm.Location('bob', '85 Prescott St, Cambridge, MA', '415-777-9999')
            delivery = pm.Delivery(api, item['description'], pickup, dropoff)
            delivery.create()


        deliveries = api.get_all_deliveries()
        return HttpResponse(deliveries)

    def get(self, request):
        return render(request, "delivery.html")

class DeliveryDataPage(TemplateView):
    def get(self, request):
        test_key = '03c270d0-d388-4c1a-8aad-468de79ecfde'
        test_id = 'cus_KUuM-I53KYnm5F'
        api = pm.PostmatesAPI(test_key, test_id)

        deliveries = api.get_all_deliveries()
        # return HttpResponse(json.dumps(deliveries))
        return render(request, "data.html", {"deliveries": deliveries, "data":random.randint(0, 5)})

class AddItemPage(TemplateView):
    def post(self, request):
        if request.method == 'POST':
            form = request.POST
            name = form['inputName']
            address = form['inputAddress']
            price = form['inputPrice']
            description = form['inputDescription']
            picture = request.FILES['item_pic']
            imagees = '/static/images/'
            #hardcoding to jack
            connection = httplib.HTTPSConnection('api.parse.com', 443)
            connection.connect()
            connection.request('POST', '/1/files/pic.jpg', open('/GarageSale/static/images/apple.jpg', 'rb').read(), {
                   "X-Parse-Application-Id": "GEhB6O9S9sJwKWRVlfcm2zghfmpN7ZIg5guhjHha",
                   "X-Parse-REST-API-Key": "Ui7OtToUquSRwLGGHxDCLB0nX9t5o2IOwSVyRjRI",
                   "Content-Type": "image/jpeg"
                 })
            result = json.loads(connection.getresponse().read())

            connection.request('POST', '/1/classes/Items', json.dumps({
                "name": name,
                "address": address,
                "price": float(price),
                "description" : description,
                "status" : "UNSOLD",
                "username" : "jack",
                "location": {
                    "__type": "GeoPoint",
                    "latitude": 42.3611,
                    "longitude": -71.2323
                },
                "picture": {
                    "name": "/1/files/pic.jpg",
                    "__type": "File"
                }
                }), {
                   "X-Parse-Application-Id": "GEhB6O9S9sJwKWRVlfcm2zghfmpN7ZIg5guhjHha",
                   "X-Parse-REST-API-Key": "Ui7OtToUquSRwLGGHxDCLB0nX9t5o2IOwSVyRjRI",
                   "Content-Type": "application/json"
                })
            results = json.loads(connection.getresponse().read())        
            return HttpResponseRedirect('/garage/')
    

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
    
    

