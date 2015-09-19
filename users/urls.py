from django.contrib.auth.decorators import login_required

from django.views.decorators.csrf import csrf_exempt
from django.conf.urls import patterns, include, url

from users import views


urlpatterns = patterns('',
    url(
            r'^login/$',
            views.LoginPage.as_view(),
            name='users_login',
        ),
        
    url(
            r'^logout/$',
            views.LogoutPage.as_view(),
            name='users_logout',
        ),
        
    url(
            r'^register/$',
            views.RegisterPage.as_view(),
            name='users_register',
        ),
        
    url(
            r'^processlog/$',
            views.ProcessLog.as_view(),
            name='users_processlog',
        ),
        
    url(
            r'^processreg/$',
            views.ProcessReg.as_view(),
            name='users_processreg',
        ),
        
    url(
            r'^test/$',
            views.LoginTestView.as_view(),
            name='users_test',
        ),
        
)

