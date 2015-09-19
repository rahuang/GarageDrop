from django.contrib.auth.decorators import login_required

from django.views.decorators.csrf import csrf_exempt
from django.conf.urls import patterns, include, url

from GarageSale.views import staff_only
from testapp import views


urlpatterns = patterns('',
    url(
            r'^echo/$',
            staff_only(views.EchoView.as_view()),
            name='test_echo',
        ),
        
    url(
            r'^500/$',
            staff_only(views.Generate500View.as_view()),
            name='test_500',
        ),
        
    url(
            r'^403/$',
            staff_only(views.Generate403View.as_view()),
            name='test_403',
        ),
        
)

