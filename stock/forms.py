# -*- coding: utf-8 -*-
import datetime

from django import forms
from django.forms import TextInput, Textarea, Select

from dal import autocomplete

from stock.models import Device, OrbitProfile, DeviceRepair, DeviceType, DeviceBrand, DeviceModel, BrokenType
from stock import models


def now():
    return datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')


class SearchForm(forms.Form):
    q = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))


class DeviceForm(forms.ModelForm):
    id = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    value = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    asset = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    sap = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '2'}), required=False)
    # An inline class to provide additional information on the form.
    class Meta:
        # Provide an association between the ModelForm and a model
        model = Device
        fields = ('id', 'type', 'name', 'model', 'sn', 'good', 'value', 'asset', 'sap', 'description')
        widgets = {
            'type': autocomplete.ModelSelect2(
                        url='devicetype-autocomplete',
                        attrs={'class': 'form-control'}
                    ),
            'name': autocomplete.ModelSelect2(
                        url='devicebrand-autocomplete',
                        attrs={'class': 'form-control'},
                        forward=['type'],
                    ),
            'model': autocomplete.ModelSelect2(
                        url='devicemodel-autocomplete',
                        attrs={'class': 'form-control'},
                        forward=['name'],
                    ),
            'sn': TextInput(attrs={'class': 'form-control'}),
            'good': Select(attrs={'class': 'form-control'}),
        }


class DeviceRepairForm(forms.ModelForm):
    id = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '2'}), required=False)

    class Meta:
        model = DeviceRepair
        fields = ('id', 'device', 'employee', 'appearance', 'judgment', 'debug', 'description')
        widgets = {
            'device': Select(attrs={'class': 'form-control'}),
            'employee': autocomplete.ModelSelect2(
                            url='employee-autocomplete',
                            attrs={'class': 'form-control'}
                        ),
            'appearance': TextInput(attrs={'class': 'form-control'}),
            'judgment': TextInput(attrs={'class': 'form-control'}),
            'debug': TextInput(attrs={'class': 'form-control'}),
        }


class OrbitProfileForm(forms.ModelForm):
    id = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    install_date = forms.DateTimeField(widget=forms.TextInput(attrs={'class': 'form-control'}), initial=now())
    company = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    telephone = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    ip = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '2'}), required=False)

    class Meta:
        model = OrbitProfile
        fields = ('id', 'device', 'version', 'company', 'telephone', 'location', 'ip', 'install_date', 'endstation', 'description')
        widgets = {
            'device': Select(attrs={'class': 'form-control'}),
            'version': TextInput(attrs={'class': 'form-control'}),
            'location': TextInput(attrs={'class': 'form-control'}),
            'endstation': TextInput(attrs={'class': 'form-control'}),
        }


class SubUnitForm(forms.Form):
    #id = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    units = forms.ModelChoiceField(widget=forms.Select(attrs={'class': 'form-control'}), queryset=None)
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '1'}), required=False)

    class Meta:
        fields = ('units', 'description')


class WarehouseForm(forms.ModelForm):
    id = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '2'}), required=False)

    class Meta:
        model = models.Warehouse
        fields = ('id', 'name', 'location', 'description')
        widgets = {
            'name': TextInput(attrs={'class': 'form-control'}),
            'location': TextInput(attrs={'class': 'form-control'}),
        }


class EmployeeForm(forms.ModelForm):
    id = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    create_date = forms.DateTimeField(widget=forms.TextInput(attrs={'class': 'form-control'}), initial=now(), required=False)
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '2'}), required=False)

    class Meta:
        model = models.Employee
        fields = ('id', 'name', 'department', 'team', 'email', 'phone', 'mobile', 'create_date', 'description')
        widgets = {
            'name': TextInput(attrs={'class': 'form-control'}),
            'department': Select(attrs={'class': 'form-control'}),
            'team': Select(attrs={'class': 'form-control'}),
            'email': TextInput(attrs={'class': 'form-control'}),
            'phone': TextInput(attrs={'class': 'form-control'}),
            'mobile': TextInput(attrs={'class': 'form-control'}),
        }


class StockinForm(forms.ModelForm):
    id = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    device = forms.ModelChoiceField(queryset=Device.objects.exclude(status=1), widget=autocomplete.ModelSelect2(url='stockin-autocomplete', attrs={'class': 'form-control'}))
    create_date = forms.DateTimeField(widget=forms.TextInput(attrs={'class': 'form-control'}), initial=now())
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '2'}), required=False)

    class Meta:
        model = models.StockIn
        fields = ['id', 'device', 'warehouse', 'employee', 'create_date', 'description']
        widgets = {
            'warehouse': Select(attrs={'class': 'form-control'}),
            'employee': autocomplete.ModelSelect2(
                            url='employee-autocomplete',
                            attrs={'class': 'form-control'}
                        ),
        }


class ApplicationForm(forms.ModelForm):
    id = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    name = forms.CharField(widget=forms.HiddenInput(), required=False, max_length=50)
    create_date = forms.DateTimeField(widget=forms.TextInput(attrs={'class': 'form-control'}), initial=now())
    approve_content = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=False, max_length=50)
    approve_date = forms.DateTimeField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=False, initial=now())
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '2'}), required=False)

    class Meta:
        model = models.Application
        fields = ('id', 'name', 'employee', 'create_date', 'approve_content', 'approve_date', 'description')
        widgets = {
            'employee': autocomplete.ModelSelect2(
                            url='employee-autocomplete',
                            attrs={'class': 'form-control'}
                        ),
        }


class ApplicationDetailForm(forms.ModelForm):
    id = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    class Meta:
        model = models.ApplicationDetail
        fields = ('id', 'device', 'number', 'location',)
        widgets = {
            #'application': Select(attrs={'class': 'form-control'}),
            'device': TextInput(attrs={'class': 'form-control'}),
            'number': TextInput(attrs={'class': 'form-control'}),
            'location': TextInput(attrs={'class': 'form-control'}),
        }


class StockoutForm(forms.ModelForm):
    id = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    application = forms.CharField(widget=TextInput(attrs={'class': 'form-control disabled'}))
    device = forms.ModelChoiceField(queryset=Device.objects.filter(status=1), widget=autocomplete.ModelSelect2(url='stockout-autocomplete', attrs={'class': 'form-control'}))
    operate_date = forms.DateTimeField(widget=forms.TextInput(attrs={'class': 'form-control'}), initial=now())
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '2'}), required=False)

    class Meta:
        model = models.StockOut
        fields = ['id', 'device', 'applicationdetail', 'operator', 'operate_date', 'description']
        widgets = {
            'applicationdetail': Select(attrs={'class': 'form-control disabled'}),
            'operator': autocomplete.ModelSelect2(
                            url='employee-autocomplete',
                            attrs={'class': 'form-control'}
                        ),
        }


class RepairForm(forms.ModelForm):
    id = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    brokentype = forms.ModelChoiceField(queryset=BrokenType.objects.all(), widget=Select(attrs={'class': 'form-control'}))
    repair_date = forms.DateTimeField(widget=forms.TextInput(attrs={'class': 'form-control'}), initial=now())
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '2'}), required=False)

    class Meta:
        model = models.DeviceRepair
        fields = ['id', 'device', 'employee', 'brokentype', 'appearance', 'judgment', 'debug', 'repair_date', 'description']
        widgets = {
            'device': autocomplete.ModelSelect2(
                            url='device-autocomplete',
                            attrs={'class': 'form-control'}
                        ),
            'employee': autocomplete.ModelSelect2(
                            url='employee-autocomplete',
                            attrs={'class': 'form-control'}
                        ),
            'brokentype': Select(attrs={'class': 'form-control'}),
            'appearance': TextInput(attrs={'class': 'form-control'}),
            'judgment': TextInput(attrs={'class': 'form-control'}),
            'debug': TextInput(attrs={'class': 'form-control'}),
        }


class RepairStatisticForm(forms.Form):
    type = forms.ModelChoiceField(widget=Select(attrs={'class': 'form-control'}),queryset=DeviceType.objects.all())
    brand = forms.ChoiceField(widget=Select(attrs={'class': 'form-control'}))
    model = forms.ChoiceField(widget=Select(attrs={'class': 'form-control'}))
    bug = forms.ChoiceField(widget=Select(attrs={'class': 'form-control'}))
    start = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control'}), initial=now())
    end = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control'}), initial=now())


class SubunitForm(forms.ModelForm):
    id = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    device = forms.ModelChoiceField(queryset=Device.objects.all(), widget=autocomplete.ModelSelect2(url='device-autocomplete', attrs={'class': 'form-control'}))
    brand = forms.ModelChoiceField(widget=Select(attrs={'class': 'form-control'}),required=False,queryset=DeviceBrand.objects.all())
    model = forms.ModelChoiceField(widget=Select(attrs={'class': 'form-control'}),required=False,queryset=DeviceModel.objects.all())
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '2'}), required=False)

    class Meta:
        model = models.SubUnit
        fields = ['id', 'name', 'sn', 'device', 'brand', 'model', 'description']
        widgets = {
            'name': Select(attrs={'class': 'form-control'}),
            'sn': TextInput(attrs={'class': 'form-control'}),
        }