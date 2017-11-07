# -*- coding: utf-8 -*-
from django.apps import AppConfig
from watson import search as watson

from stock import models
from stock import adapters


class MyAppConfig(AppConfig):
    name = 'stock'

    def ready(self):
        watson.register(models.Warehouse, adapters.WarehouseAdapter)
        watson.register(models.Employee, adapters.EmployeeAdapter)
        watson.register(models.Device, adapters.DeviceAdapter)
        watson.register(models.SubUnit, adapters.SubunitAdapter)
        watson.register(models.StockIn, adapters.StockinAdapter)
        watson.register(models.Application, adapters.ApplicationAdapter)
        watson.register(models.StockOut, adapters.StockoutAdapter)
        watson.register(models.DeviceRepair, adapters.DeviceRepairAdapter)
