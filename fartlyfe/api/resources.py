from django.conf.urls import url
from django.template.defaultfilters import time
from django.contrib.auth.models import User
from tastypie.resources import ModelResource
from tastypie.utils import trailing_slash

from apps.local_calendar.models import LocalEvent
from apps.blogs.models import Blog, Entry


class EventResource(ModelResource):
    class Meta:
        queryset = LocalEvent.objects.filter(approved=True)
        resource_name = 'events'
        allowed_methods = ['get', 'post',]

    def dehydrate(self, bundle):
        bundle.data['days'] = []
        return bundle

class BlogResource(ModelResource):
    class Meta:
        queryset = Blog.objects.filter(public=True)
        allowed_methods = ['get',]


    
