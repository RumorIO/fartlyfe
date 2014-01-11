from django import template
from django.core.urlresolvers import reverse  
from django.template.loader import render_to_string
from django.template.defaultfilters import time, date
from django.http import HttpResponse

import datetime
import simplejson


register = template.Library()

@register.filter
def json_info(location):
    info = {}
    info['latitude'] = location.latitude
    info['longitude'] = location.longitude
    info['name'] = location.name
    info['address'] = ' '.join(location.get_full_address())
    return simplejson.dumps(info, cls=simplejson.encoder.JSONEncoderForHTML)

@register.simple_tag  
def api_detail(resource_name, pk):  
    """Return API URL for Tastypie Resource details.

    Usage::

        {% api_detail 'entry' entry.pk %}

    or::

        {% api_detail 'api2:entry' entry.pk %}  
    """  
    if ':' in resource_name:  
        api_name, resource_name = resource_name.split(':', 1)  
    else:  
        api_name = 'api'  
    return reverse('api_dispatch_detail', kwargs={  
            'api_name': api_name,  
            'resource_name': resource_name,  
            'pk': pk  
        }) + '?format=json'

