from django.conf.urls import patterns, include, url

from apps.feeds.models import Post
from apps.feeds.views import BlogListView, PostListView

urlpatterns = patterns('',
    url(r'^$', BlogListView.as_view(), name='feeds_all'),
    url(r'^listen/$', BlogListView.as_view(), name='feeds_listen'),
    url(r'^read/$', BlogListView.as_view(), name='feeds_read'),
    url(r'^watch/$', BlogListView.as_view(), name='feeds_watch'),
    url(r'^(?P<slug>[-\w0-9]+)/$', PostListView.as_view(), name='blog_post_list'),
    url(r'^archive/', include('apps.feeds.urls.archives')), 
    
)    
