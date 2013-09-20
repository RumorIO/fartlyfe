from django.conf.urls.defaults import *

import apps.search
from apps.blog.models import Entry
from apps.blog.views import BlogFrontView, stop_errors

urlpatterns = patterns('',
    url(r'^$', 
        BlogFrontView.as_view(), 
        name='blog_front'),
    (r'^search/$', include('apps.search.urls')),
    (r'^archive/', include('apps.blog.urls.archives')), 
    (r'^category/', include('apps.blog.urls.categories')),
    url(r'^wp-login.php$', 'stop_errors', name = 'stop_errors'),
)    
