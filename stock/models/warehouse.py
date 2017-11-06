# -*- coding: utf-8 -*-
from django.db import models

from auditlog.registry import auditlog

from common import CommonInfo

class Warehouse(CommonInfo):
    name = models.CharField(max_length=30, unique=True, verbose_name=u"名称", db_index=True)
    location = models.CharField(max_length=50, unique=True, verbose_name=u"位置")

    def __unicode__(self):
        return self.name + ' ' + self.location

    def get_warehouse_dispaly(self):
        return self.name

    def dict(self):
        d = {'id': self.id,
             'name': self.name,
             'location': self.location}
        d.update(super(Warehouse, self).dict())
        return d

    class Meta:
        verbose_name = u'库房表'
        verbose_name_plural = u'库房表'


auditlog.register(Warehouse)


class Shelf(CommonInfo):
    name = models.CharField(max_length=30, unique=True, verbose_name=u"名称", db_index=True)
    parent = models.ForeignKey(Warehouse, verbose_name=u"所在库房")

    def __unicode__(self):
        return self.parent.name + '/' + self.name

    def get_shelf_dispaly(self):
        return self.name

    class Meta:
        verbose_name = u'库房货架表'
        verbose_name_plural = u'库房货架表'


auditlog.register(Shelf)


class Layer(CommonInfo):
    name = models.CharField(max_length=30, unique=True, verbose_name=u"名称", db_index=True)
    parent = models.ForeignKey(Shelf, verbose_name=u"所在货架")

    def __unicode__(self):
        return self.parent.name + '/' + self.name

    def get_layer_dispaly(self):
        return self.name

    class Meta:
        verbose_name = u'货架层次表'
        verbose_name_plural = u'货架货架表'


auditlog.register(Layer)