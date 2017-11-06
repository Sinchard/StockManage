# -*- coding: utf-8 -*-
from django.db import models

from auditlog.models import AuditlogHistoryField

from stock.utils import time2str

class CommonInfo(models.Model):
    check_choice=(
        (True,u'已审核'),
        (False,u'未审核'),
    )
    history = AuditlogHistoryField()

    attach = models.FileField(upload_to='attachment/%Y/%m/%d', verbose_name='附件', null=True)
    check = models.BooleanField(default=False, choices=check_choice, verbose_name=u"是否审核")
    create_date = models.DateTimeField(blank=True, null=True, auto_now_add=True, verbose_name=u"创建时间")
    modify_date = models.DateTimeField(blank=True, null=True, auto_now=True, verbose_name=u"修改时间")
    description = models.CharField(max_length=100, blank=True, null=True, verbose_name=u"备注")

    def dict(self):
        return {'create_date': time2str(self.create_date), 'check': self.check,
                'description': self.description}

    @property
    def created(self):
        return time2str(self.create_date)

    def get_create_date_display(self):
        return time2str(self.create_date)

    class Meta:
        app_label = 'stock'
        abstract = True
        ordering = ['-modify_date']