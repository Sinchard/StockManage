# -*- coding: utf-8 -*-
from django.db import models

from auditlog.registry import auditlog

from common import CommonInfo
from warehouse import Warehouse
from employee import Employee
from stock.utils import *


class DeviceType(CommonInfo):
    name = models.CharField(max_length=30, unique=True, verbose_name=u"名称", db_index=True)

    def __unicode__(self):
        return self.name

    def get_type_display(self):
        return self.name

    def dict(self):
        d = {'id': self.id,
             'name': self.name}
        d.update(super(DeviceType, self).dict())
        return d

    class Meta:
        verbose_name = u'设备类型表'
        verbose_name_plural = u'设备类型表'


auditlog.register(DeviceType)


class DeviceBrand(CommonInfo):
    name = models.CharField(max_length=30, unique=True, verbose_name=u"名称", db_index=True)
    parent = models.ForeignKey(DeviceType, null=True, verbose_name=u"设备类型")

    def __unicode__(self):
        return self.name

    def get_brand_display(self):
        return self.name

    def dict(self):
        d = {'id': self.id,
             'name': self.name,
             'parentId': self.parent.id,
             'parent': self.parent.name}
        d.update(super(DeviceBrand, self).dict())
        return d

    class Meta:
        verbose_name = u'设备品牌表'
        verbose_name_plural = u'设备品牌表'


auditlog.register(DeviceBrand)


class DeviceModel(CommonInfo):
    name = models.CharField(max_length=30, unique=True, verbose_name=u"名称", db_index=True)
    parent = models.ForeignKey(DeviceBrand, null=True, verbose_name=u"设备品牌")

    def __unicode__(self):
        return self.name

    def get_model_display(self):
        return self.name

    def dict(self):
        d = {'id': self.id,
             'name': self.name,
             'parentId': self.parent.id,
             'parent': self.parent.name}
        d.update(super(DeviceModel, self).dict())
        return d

    class Meta:
        verbose_name = u'设备型号表'
        verbose_name_plural = u'设备型号表'


auditlog.register(DeviceModel)


class DeviceSubUnit(CommonInfo):
    name = models.CharField(max_length=30, verbose_name=u"名称", db_index=True)
    parent = models.ForeignKey(DeviceModel, null=True, verbose_name=u"设备型号")

    def __unicode__(self):
        return self.parent.name + '/' + self.name

    def dict(self):
        d = {'id': self.id,
             'name': self.name,
             'parentId': self.parent.id,
             'parent': self.parent.name}
        d.update(super(DeviceModel, self).dict())
        return d

    class Meta:
        verbose_name = u'设备组件表'
        verbose_name_plural = u'设备组件表'


auditlog.register(DeviceSubUnit)


class Device(CommonInfo):
    status_choice = (
        (1, u'在库中'),
        (2, u'已出库且可控'),
        (3, u'已出库不可控'),
        (4, u'未知'),
        (5, u'已划拨'),
    )
    good_choice = (
        (1, u'故障'),
        (5, u'良好'),
    )
    name = models.ForeignKey(DeviceBrand, null=True, verbose_name=u"名称")
    model = models.ForeignKey(DeviceModel, null=True, verbose_name=u"型号")
    sn = models.CharField(max_length=100, verbose_name=u"设备编码", db_index=True)
    type = models.ForeignKey(DeviceType, null=True, verbose_name=u"类型")
    # subunit = models.BooleanField(default=False, verbose_name=u"是否为配件")
    good = models.IntegerField(default=5, choices=good_choice, verbose_name=u"设备状态")
    value = models.DecimalField(default=0, max_digits=10, decimal_places=2, verbose_name=u"价格")
    asset = models.CharField(max_length=100, blank=True, null=True, verbose_name=u"资产编码")
    sap = models.CharField(max_length=100, blank=True, null=True, verbose_name=u"SAP")
    status = models.IntegerField(default=4, choices=status_choice, verbose_name=u"状态")
    warehouse = models.ForeignKey(Warehouse, blank=True, null=True, verbose_name=u"所在库房")
    location = models.CharField(max_length=50, blank=True, null=True, verbose_name=u"位置")

    def __unicode__(self):
        return self.name.name + '/' + self.model.name + '/' + self.sn  # + ' ' + self.type.name

    def get_device_display(self):
        return u'{0}/{1}/{2}'.format(self.name.name, self.model.name, self.sn)

    def get_type_display(self):
        if self.type:
            return self.type.get_type_display()
        else:
            return ""

    def autocomplateFormate(self):
        return {'label': self.name.name + '/' + self.model.name + '/' + self.sn, 'value': self.id}

    def dict(self):
        if self.warehouse == None:
            self.warehouse = Warehouse(id=0, name='')

        d = {'id': self.id,
             'sn': self.sn,
             'name': self.name.name, 'nameId': self.name.id,
             'model': self.model.name, 'modelId': self.model.id,
             'type': self.type.name, 'typeId': self.type.id,
             'good': str(self.good),
             'asset': self.asset,
             'sap': self.sap,
             'status': self.status,
             'warehouse': self.warehouse.name, 'warehouseId': self.warehouse.id,
             'location': self.location}
        d.update(super(Device, self).dict())
        return d

    class Meta:
        verbose_name = u'设备表'
        verbose_name_plural = u'设备表'


auditlog.register(Device)


class SubUnit(CommonInfo):
    brand = models.ForeignKey(DeviceBrand, null=True, verbose_name=u"名称")
    model = models.ForeignKey(DeviceModel, null=True, verbose_name=u"型号")
    device = models.ForeignKey(Device, null=True, verbose_name=u"所属设备")
    name = models.ForeignKey(DeviceSubUnit, verbose_name=u"名称")
    sn = models.CharField(max_length=100, verbose_name=u"组件序列号", db_index=True)

    def __unicode__(self):
        return self.name.name + ' : ' + self.sn

    def get_device_display(self):
        if self.device:
            return self.device.get_device_display()
        else:
            return ''

    def get_name_display(self):
        if self.name:
            return self.name.name
        else:
            return ''

    def get_brand_display(self):
        if self.brand:
            return self.brand.name
        else:
            return ''

    def get_model_display(self):
        if self.model:
            return self.model.name
        else:
            return ''

    class Meta:
        verbose_name = u'组件表'
        verbose_name_plural = u'组件表'


auditlog.register(SubUnit)


class OrbitProfile(CommonInfo):
    device = models.ForeignKey(Device, verbose_name=u"设备")
    version = models.CharField(max_length=50, null=True, verbose_name=u"系统版本")
    location = models.CharField(max_length=50, verbose_name=u"安装位置")
    company = models.CharField(max_length=50, null=True, verbose_name=u"船舶所属")
    telephone = models.CharField(max_length=50, null=True, verbose_name=u"联系电话")
    ip = models.CharField(max_length=50, null=True, verbose_name=u"室内外IP地址")
    install_date = models.DateTimeField(blank=True, null=True, verbose_name=u"安装时间")
    endstation = models.CharField(max_length=30, null=True, verbose_name=u"端站ID", db_index=True)

    def __unicode__(self):
        return self.device.name.name + ',' + self.device.model.name + ',' + self.device.sn + ':' + self.version + ',' + self.location

    def get_install_date_display(self):
        return time2str(self.install_date)

    def get_device_display(self):
        if self.device:
            return self.device.get_device_display()
        else:
            return ''

    def get_device_id_display(self):
        if self.device:
            return self.device.id
        else:
            return 0

    def dict(self):
        d = {'id': self.id,
             'deviceId': self.device.id,
             'device': self.device.name.name + ',' + self.device.model.name + ',' + self.device.sn,
             'location': self.location, 'install_date': self.install_date,
             'endstation': self.endstation}
        return d

    class Meta:
        verbose_name = u'Orbit信息表'
        verbose_name_plural = u'Orbit信息表'


auditlog.register(OrbitProfile)


class BrokenType(CommonInfo):
    devicemodel = models.ForeignKey(DeviceModel)
    unit = models.ForeignKey(DeviceSubUnit, null=True)
    name = models.CharField(max_length=100, db_index=True)

    def __unicode__(self):
        return self.name

    def dict(self):
        d = {'id': self.id,
             'modelId': self.devicemodel.id, 'modelName': self.devicemodel.name,
             'name': self.name}
        return d

    class Meta:
        verbose_name = u'故障类型表'
        verbose_name_plural = u'故障类型表'


auditlog.register(BrokenType)


class DeviceRepair(CommonInfo):
    device = models.ForeignKey(Device)
    employee = models.ForeignKey(Employee)
    brokentype = models.ForeignKey(BrokenType)
    appearance = models.CharField(max_length=100, verbose_name=u"故障现象")
    judgment = models.CharField(max_length=100, verbose_name=u"故障判断")
    debug = models.CharField(max_length=100, verbose_name=u"故障处理", db_index=True)
    repair_date = models.DateTimeField(null=True, verbose_name=u"修理时间")

    def __unicode__(self):
        return self.appearance + self.debug

    def dict(self):
        d = {'id': self.id,
             'deviceId': self.device.id,
             'device': self.device.name.name + ',' + self.device.model.name + ',' + self.device.sn,
             'employeeId': self.employee.id, 'employee': self.employee.name,
             'brokentype': self.get_brokentype_display(),
             'appearance': self.appearance,
             'judgment': self.judgment,
             'debug': self.debug,
             'repair_date': time2str(self.repair_date)}
        d.update(super(DeviceRepair, self).dict())
        return d

    def get_device_display(self):
        if self.device:
            return self.device.get_device_display()
        else:
            return ''

    def get_employee_display(self):
        if self.device:
            return self.employee.name
        else:
            return ''

    def get_brokentype_display(self):
        if self.brokentype:
            return self.brokentype.name
        else:
            return ''

    def get_repair_date_display(self):
        return time2str(self.repair_date)

    class Meta:
        verbose_name = u'故障处理表'
        verbose_name_plural = u'故障处理表'
        ordering = ['-repair_date']


auditlog.register(DeviceRepair)
