from django.conf.urls import patterns, include, url
from django.views.generic import ListView, DetailView

from endless_pagination.views import AjaxListView

from apps.feeds.models import Post, Feed
from apps.feeds.views import FeedTopArchiveView, FeedYearArchiveView, FeedMonthArchiveView, PostDetailView
 
urlpatterns = patterns('',
    url(r'^$', AjaxListView.as_view(
                            model = Feed,
                            template_name = 'feeds/feed_list.html',
                            page_template = 'feeds/feed_list_page.html',
                            queryset = Feed.published.all(),), name='all_feeds'),
    
    url(r'^read/$', AjaxListView.as_view(
                            model = Feed,
                            template_name = 'feeds/feed_list.html',
                            page_template = 'feeds/feed_list_page.html',
                            queryset = Feed.published.filter(post__media='').distinct(),), name='read_feeds'),
    
    url(r'^listen/$', AjaxListView.as_view(
                            model = Feed,
                            template_name = 'feeds/feed_list.html',
                            page_template = 'feeds/feed_list_page.html',
                            queryset = Feed.published.filter(post__mimetype__icontains='audio').distinct(),), name='listen_feeds'),
    
    url(r'^watch/$', AjaxListView.as_view(
                            model = Feed,
                            template_name = 'feeds/feed_list.html',
                            page_template = 'feeds/feed_list_page.html',
                            queryset = Feed.published.filter(post__mimetype__icontains='video').distinct(),), name='watch_feeds'),


    url(r'^tags/', include('apps.feeds.urls.tags')),
    url(r'^topics/', include('apps.feeds.urls.topics')),
    url(r'', include('apps.feeds.urls.archives')),

)


