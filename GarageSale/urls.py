from django.conf.urls import patterns, include, url
from django.contrib import admin

from GarageSale import views

# Override the Admin Site header
admin.site.site_header = "Django Template Administration"

# Set the error handlers
handler403 = views.PermissionDeniedView.as_view()
handler404 = views.NotFoundView.as_view()
handler500 = views.ErrorView.as_view()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'GarageSale.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    
    url(r'^$', views.IndexPage.as_view(), name='index'),
    url(r'^login/', views.LoginPage.as_view(), name='login'),
    url(r'^garage/$', views.GaragePage.as_view(), name='garage'),
    url(r'^orders/$', views.OrdersPage.as_view(), name='orders'),
    url(r'^account/$', views.AccountPage.as_view(), name='account'),
    url(r'^mycart/$', views.MyCartPage.as_view(), name='mycart'),

    

    url(r'^test/', include('testapp.urls')),
    url(r'^users/', include('users.urls')),
    
    url(r'^admin/', include(admin.site.urls)),
)
