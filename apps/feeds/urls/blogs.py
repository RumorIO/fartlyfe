from django.conf.urls.defaults import *

from apps.feeds.models import Post
from apps.feeds.views import BlogListView, PostListView

urlpatterns = patterns('',
    url(r'^$', BlogListView.as_view(), name='all_blog_list'),
    url(r'^(?P<slug>[-\w0-9]+)/$', PostListView.as_view(), name='blog_post_list'),
    url(r'^archive/', include('apps.feeds.urls.archives')), 
    
)    
