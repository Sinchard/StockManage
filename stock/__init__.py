# -*- coding: utf-8 -*-
default_app_config = 'stocks.apps.MyAppConfig'

from stock.models import Employee

appInfo = {'title': u'库存管理系统', 'appname': u'库存管理系统'}


def updateUserInfo(id):
    try:
        employee = Employee.objects.get(user_id=id)
        name = employee.name
        role = employee.role_id
        appInfo.update({'leader': role > 1, 'name': name, 'manager': role>3, 'id':employee.id})
    except Exception as e:
        print e
