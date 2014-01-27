from django.conf.urls import patterns, include, url
from django.views.generic.dates import YearArchiveView, MonthArchiveView 

from endless_pagination.views import AjaxListView

from apps.feeds.models import Post
from apps.feeds.views import PostsByFeedView, FeedTopArchiveView, FeedYearArchiveView, FeedMonthArchiveView, PostDetailView
 
urlpatterns = patterns('',
    
    url(r'^(?P<slug>[-\w\d]+)/$', PostsByFeedView.as_view(), name='posts_by_feed'),
    url(r'^(?P<slug>[-\w\d]+)/archive/$', FeedTopArchiveView.as_view(), name='archive_top'),
    url(r'^(?P<slug>[-\w\d]+)/(?P<year>\d{4})/$', YearArchiveView.as_view(), name='year_posts'),
    url(r'^(?P<slug>[-\w\d]+)/(?P<year>\d{4})/(?P<month>\w{3})/$', FeedMonthArchiveView.as_view(), name='month_posts'),
    url(r'^(?P<feed>[-\w\d]+)/(?P<year>\d{4})/(?P<month>\w{3})/(?P<day>\d{2})/(?P<slug>[-\w\d]+)/$', PostDetailView.as_view(), name='post_detail'),

    
    #url(r'^(?P<slug>[-\w\d]+)/subscribe/rss.xml$', RSSFeed(), name="feed-rss"),
    #url(r'^(?P<slug>[-\w\d]+)/subscribe/atom.xml$', AtomFeed(), name="atom-rss"),
    #url(r'^(?P<slug>[-\w\d]+)/subscribe/podcast.xml$', PodcastFeed(), name="podcast-rss"),
)
