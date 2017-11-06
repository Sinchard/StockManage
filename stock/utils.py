# -*- coding: utf-8 -*-

import datetime

from django.http import HttpResponse
from django_jinja.backend import Jinja2

def time2str(d):
    if d:
        str=datetime.datetime.strftime(d,'%Y-%m-%d %H:%M:%S')
    else:
        str=''
    return str

def str2time(s):
    try:
        d=datetime.datetime.strptime(s, '%Y-%m-%d %H:%M:%S')
    except Exception,e:
        d=None
    finally:
        return d


def render_to_response(filename, context={}):
    template = Jinja2({}).get_template(filename)
    rendered = template.render(**context)
    return HttpResponse(rendered)