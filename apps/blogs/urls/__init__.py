from django.conf.urls import patterns, include, url

import apps.search
from apps.blogs.models import Entry
from apps.blogs.views import BlogListView, BlogPostListView

urlpatterns = patterns('',
    url(r'^$', BlogListView.as_view(), name='all_blog_list'),
    url(r'^(?P<blog>[-\w0-9]+)/$', BlogPostListView.as_view(), name='blog_post_list'),
    url(r'^search/$', include('apps.search.urls')),
    url(r'^archive/', include('apps.blogs.urls.archives')), 
    #url(r'^category/', include('apps.blogs.urls.categories')),
 
)    
