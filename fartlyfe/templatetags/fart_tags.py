from django import template
from django.db.models import Count, Q
from django.template.loader import render_to_string

import datetime
import json

from apps.feeds.models import Feed, Post

register = template.Library()

@register.inclusion_tag('template_tag/list.html')
def item_list(*args, **kwargs):
    if kwargs.has_key('list'):
        object_list = kwargs['list']
    else:
        object_list = []
    if kwargs.has_key('parent'):
        parent = kwargs['parent']
    else:
        parent = ''
    if kwargs.has_key('number'):
        number = int(kwargs['number'])
    else:
        number = 4
    return {
            'object_list' : object_list[:number],
            'parent' : parent,
            'number' : number,}


@register.filter
def doc(value):
    return value.__doc__


@register.filter
def json_info(location):
    info = {}
    info['latitude'] = location.latitude
    info['longitude'] = location.longitude
    info['name'] = location.name
    info['address'] = ' '.join(location.get_full_address())
    return json.dumps(info)


@register.filter
def get_month_cover_url(value, slug):
    year = value.strftime('%Y')
    month = value.strftime('%m')
    posts = Post.live.filter(feed__slug=slug).filter(pub_date_year__year=year, pub_date_year__month=month)
    first = posts[0]
    #return first.cover.get_list_url
    return ''


