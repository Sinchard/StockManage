# -*- coding: utf-8 -*-
from __future__ import absolute_import

import copy
import json
from django.contrib.auth.decorators import permission_required

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, render

from stock.models import Warehouse
from stock import appInfo, updateUserInfo
from stock.forms import WarehouseForm


def ShowWarehouse(request):
    #if request.user.is_active:
        updateUserInfo(request.user.id)
        dict = copy.copy(appInfo)
        return render_to_response('stock/warehouse.html', dict, using='jinja2')
    #else:
        #return HttpResponseRedirect('login.html')


@permission_required('stocks.change_warehouse')
def SaveWarehouse(request, id):
    alert = 'F'
    new=False
    w=None
    try:
        w=Warehouse.objects.get(id=id)
    except Exception as e:
        print e

    if request.method == 'POST':  # A HTTP POST?
        form = WarehouseForm(request.POST,instance=w)
        # Have we been provided with a valid form?
        if form.is_valid():
            # Save the new category to the database.
            device = form.save(commit=True)
            alert = 'T'
            if id == u'0':
                return HttpResponseRedirect('/stocks/warehouse/' + str(device.id) + '/detail.html')
        else:
            # The supplied form contained errors - just print them to the terminal.
            print form.errors
    else:
        # If the request was not a POST, display the form to enter details.
        alert = 'N'
        form = None
        try:
            warehouse = Warehouse.objects.get(id=id)
            form = WarehouseForm(instance=warehouse)
        except Exception as e:
            print e
            form = WarehouseForm()
            new=True

    updateUserInfo(request.user.id)
    dict = copy.copy(appInfo)
    dict.update({'form': form, 'alert': alert, 'new':new})
    return render(request, 'stock/warehouse_detail.html', dict, using='jinja2')


@permission_required('stocks.delete_warehouse')
def DeleteWarehouse(request, id):
    status = {'status': 'success'}
    try:
        w = Warehouse.objects.get(id=id)
        w.delete()
    except Exception:
        status['status'] = 'error'
    return HttpResponse(json.dumps(status))
