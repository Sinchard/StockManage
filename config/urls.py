"""StockManage URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin

from stock.views import warehouse

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    # userena
    url(r'^accounts/', include('userena.urls')),

    # Warehouse
    url(r'^warehouse.html$', warehouse.ShowWarehouse, name='ShowWarehouse'),
    #url(r'^warehouselist$', warehouse.WarehouseList.as_view(), name='WarehouseList'),
    url(r'^warehouse/(?P<id>[\w\-]+)/detail.html$', warehouse.SaveWarehouse, name='SaveWarehouse'),
    url(r'^warehouse/(?P<id>[\w\-]+)/delete.html$', warehouse.DeleteWarehouse, name='DeleteWarehouse'),
]
