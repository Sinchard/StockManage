# -*- coding: utf-8 -*-
import datetime

from watson import search as watson

from stock.models import Device, ApplicationDetail, Application

def strftime(time):
    return datetime.datetime.strftime(time, '%Y-%m-%d %H:%M:%S')

class WarehouseAdapter(watson.SearchAdapter):
    def get_content(self, obj):
        content = u"名称:{0},位置:{1}".format(obj.name,obj.location)
        if obj.description:
            content +=u",备注："+obj.description
        return content

    def get_url(self, obj):
        return "/stocks/warehouse/"+str(obj.id)+"/detail.html"


class EmployeeAdapter(watson.SearchAdapter):
    def get_content(self, obj):
        content = u"用户名:{0},部门:{1},班组:{2},电子邮箱:{3}".format(obj.name,obj.department.name,obj.team.name,obj.email)
        if obj.phone:
            content +=u",座机:"+obj.phone
        if obj.mobile:
            content +=u",手机:"+obj.mobile
        if obj.description:
            content +=u",备注:"+obj.description
        return content

    def get_url(self, obj):
        return "/stocks/employee/"+str(obj.id)+"/detail.html"


class DeviceAdapter(watson.SearchAdapter):
    def get_content(self, obj):
        content = u"类型:{0},品牌:{1},型号:{2},序列号:{3},评分:{4},购买价格:{5}".format(obj.type.name,obj.name.name,obj.model.name,obj.sn,obj.good,obj.value)
        if obj.asset:
            content +=u",资产编码:"+obj.asset
        if obj.sap:
            content +=u",SAP:"+obj.sap
        content +=u",状态:"+Device.status_choice[obj.status-1][1]
        if obj.status==1:
            content +=u",所在库房:"+obj.warehouse.name
        elif obj.status==2 or obj.status==3:
            content +=u",安装位置:"+obj.location
        if obj.description:
            content +=u",备注:"+obj.description
        return content

    def get_url(self, obj):
        return "/stocks/device/"+str(obj.id)+"/detail.html"


class SubunitAdapter(watson.SearchAdapter):
    def get_content(self, obj):
        content = u"名称:"+obj.name.name
        if obj.brand:
            content +=u",品牌:"+obj.brand.name
        if obj.model:
            content +=u",型号:"+obj.model.name
        content += u",序列号:"+obj.sn
        if obj.device:
            content +=u",所属设备:{0}/{1}/{2}".format(obj.device.name.name,obj.device.model.name,obj.device.sn)
        if obj.description:
            content +=u",备注:"+obj.description
        return content

    def get_url(self, obj):
        return "/stocks/subunit/"+str(obj.id)+"/detail.html"


class OrbitAdapter(watson.SearchAdapter):
    def get_content(self, obj):
        content =u"设备信息:{0}/{1}/{2}".format(obj.device.name.name,obj.device.model.name,obj.device.sn)
        if obj.version:
            content +=u",系统版本:"+obj.version
        if obj.location:
            content +=u",安装位置:"+obj.location
        if obj.company:
            content +=u",船舶所属:"+obj.company
        if obj.telephone:
            content +=u",联系电话:"+obj.telephone
        if obj.install_date:
            content +=u",安装时间:"+strftime(obj.install_date)
        if obj.endstation:
            content +=u",端站ID:"+obj.endstation
        if obj.description:
            content +=u",备注:"+obj.description
        return content

    def get_url(self, obj):
        return "/stocks/orbit/"+str(obj.id)+"/detail.html"


class DeviceRepairAdapter(watson.SearchAdapter):
    def get_content(self, obj):
        content =u"设备信息:{0}/{1}/{2}".format(obj.device.name.name,obj.device.model.name,obj.device.sn)
        content +=u",故障现象:{0},故障判断:{1},故障处理:{2}".format(obj.appearance,obj.judgment,obj.debug)
        content +=u",处理人:"+obj.employee.name
        if obj.description:
            content +=u",备注:"+obj.description
        return content

    def get_url(self, obj):
        return "/stocks/repair/"+str(obj.id)+"/detail.html"


class StockinAdapter(watson.SearchAdapter):
    def get_content(self, obj):
        content =u"设备信息:{0}/{1}/{2}".format(obj.device.name.name,obj.device.model.name,obj.device.sn)
        content +=u",库房名称:"+obj.warehouse.name
        content +=u",入库人:"+obj.employee.name
        content +=u",入库时间:"+strftime(obj.create_date)
        if obj.description:
            content +=u",备注:"+obj.description
        return content

    def get_url(self, obj):
        return "/stocks/stockin/"+str(obj.id)+"/detail.html"


class ApplicationAdapter(watson.SearchAdapter):
    def get_content(self, obj):
        if obj and obj.name and obj.name!='new':
            content =u"申请人:"+obj.employee.name
            content +=u",申请时间:"+strftime(obj.create_date)
            details = ApplicationDetail.objects.filter(application=obj)
            if len(details)>0:
                content +=u",申请详情:"
            for d in details:
                if d.device:
                    content += u"{0}/{1}/{2},".format(d.device,d.number,d.location)
            content += u"当前状态:"+Application.status_choice[obj.status][1]
            if obj.status>=2:
                content += u",审批意见:"+obj.approve_content
                content += u",审批时间:"+strftime(obj.approve_date)
            if obj.status==4:
                content += u",确认人:"+obj.confirm.name
                content += u",确认内容:"+obj.confirm_content
                content += u",确认时间:"+strftime(obj.confirm_date)
            if obj.description:
                content +=u",备注:"+obj.description
            return content
        else:
            return ""

    def get_url(self, obj):
        return "/stocks/application/"+str(obj.id)+"/detail.html"


class StockoutAdapter(watson.SearchAdapter):
    def get_content(self, obj):
        if obj.device:
            content =u"设备信息:{0}/{1}/{2}".format(obj.device.name.name,obj.device.model.name,obj.device.sn)
            content += u",设备申请名称:{0},设备去向:{1},出库人:{2},出库时间:{3}".format(obj.applicationdetail.application.name,obj.location,obj.operator.name,strftime(obj.operate_date))
            if obj.description:
                content +=u",备注:"+obj.description
            return content
        else:
            return ""

    def get_url(self, obj):
        return "/stocks/stockout/"+str(obj.id)+"/detail.html"


