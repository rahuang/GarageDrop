import sys
import requests
import postmates

from django.core.exceptions import PermissionDenied
from django.http import (HttpResponse, HttpResponseNotFound,
    HttpResponseBadRequest, HttpResponseServerError)
from django.views.generic.base import View
from django.views.generic import TemplateView
from django.shortcuts import render
from django.contrib.auth.views import redirect_to_login

from GarageSale.forms import DeliveryQuoteForm



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
    template_name = 'index.html'

class GaragePage(TemplateView):
    """ The Garage Page. """
    template_name = 'garage.html'

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
    
    
def getQuote(request):
    test_key = '489913f8-8da9-431b-b2d3-05b013c87077'
    test_id = 'cus_KUqEcMmgrhGHH-'

    if request.method == 'POST':
        form = DeliveryQuoteForm(request.POST)
        if form.is_valid():
            pickup_address = (form.cleaned_data['start_addr'] + ", " +
                        form.cleaned_data['start_city'] + ", " +
                        form.cleaned_data['start_state'] + " "+
                        form.cleaned_data['start_zip'])
            dropoff_address = (form.cleaned_data['end_addr'] + ", " +
                        form.cleaned_data['end_city'] + ", " +
                        form.cleaned_data['end_state'] + " "+
                        form.cleaned_data['end_zip'])

            
                                headers={"dropoff_address" : dropoff_address, "pickup_address" : pickup_address})
            api = postmates.PostmatesAPI(test_key, test_id)
            s = str(r.status_code)
            return HttpResponse(s)


    else:
        form = DeliveryQuoteForm()

    return render (request, 'getQuote.html' , {'form' : form})
