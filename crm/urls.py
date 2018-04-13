from django.conf.urls import  url
from . import views

urlpatterns = [
    url(r'^$', views.CustomerSearchView.as_view(), name='customers_search'),
    url(r'^customer/(?P<pk>\d+)/$', views.CustomerDetailView.as_view(), name='customers_detail'),
    url(r'^create$', views.CustomerCreateView.as_view(), name='customers_create'),
]