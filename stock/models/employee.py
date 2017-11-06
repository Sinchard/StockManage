# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

from auditlog.registry import auditlog

from common import CommonInfo

class Department(CommonInfo):
    name = models.CharField(max_length=30, unique=True, verbose_name=u"名称", db_index=True)

    def __unicode__(self):
        return self.name

    def dict(self):
        d = {'id': self.id,
             'name': self.name}
        d.update(super(Department, self).dict())
        return d

    class Meta:
        verbose_name = u'部门表'
        verbose_name_plural = u'部门表'


auditlog.register(Department)


class Team(CommonInfo):
    name = models.CharField(max_length=30, unique=True, verbose_name=u"名称", db_index=True)
    department = models.ForeignKey(Department, verbose_name=u"所属部门")

    def __unicode__(self):
        return self.name

    def dict(self):
        d = {'id': self.id,
             'name': self.name,
             'departmentId': self.department.id, 'department': self.department.name}
        d.update(super(Team, self).dict())
        return d

    class Meta:
        verbose_name = u'班组表'
        verbose_name_plural = u'班组表'


auditlog.register(Team)


class Role(CommonInfo):
    name = models.CharField(max_length=30, unique=True, verbose_name=u"名称", db_index=True)

    def __unicode__(self):
        return self.name

    def dict(self):
        d = {'id': self.id,
             'name': self.name}
        d.update(super(Role, self).dict())
        return d

    class Meta:
        verbose_name = u'角色表'
        verbose_name_plural = u'角色表'


auditlog.register(Role)


class Employee(CommonInfo):
    user = models.OneToOneField(User, null=True)
    name = models.CharField(max_length=30, unique=True, verbose_name=u"姓名", db_index=True)
    department = models.ForeignKey(Department, verbose_name=u"部门")
    team = models.ForeignKey(Team, verbose_name=u"班组")
    role = models.ForeignKey(Role, verbose_name=u"角色")
    email = models.EmailField(unique=True, verbose_name=u"邮箱")
    phone = models.CharField(max_length=30, null=True, verbose_name=u"手机号码")
    mobile = models.CharField(max_length=30, null=True, verbose_name=u"座机号码")

    def __unicode__(self):
        return self.name

    def get_employee_display(self):
        return self.name

    def get_department_display(self):
        if self.department:
            return self.department.name
        else:
            return ""

    def get_team_display(self):
        if self.team:
            return self.team.name
        else:
            return ""

    def get_role_display(self):
        if self.role:
            return self.role.name
        else:
            return ""

    def dict(self):
        d = {'id': self.id,
             'name': self.name,
             'department': self.department.name, 'departmentId': self.department.id,
             'team': self.team.name, 'teamId': self.team.id,
             'role': self.role.name, 'roleId': self.role.id,
             'email': self.email,
             'phone': self.phone}
        d.update(super(Employee, self).dict())
        return d

    class Meta:
        verbose_name = u'员工表'
        verbose_name_plural = u'员工表'


auditlog.register(Employee)