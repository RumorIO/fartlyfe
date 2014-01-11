from django.conf.urls import patterns, include, url

from apps.feeds.models import Post
from apps.feeds.views import FeedTopArchiveView, FeedYearArchiveView, FeedMonthArchiveView, PostDetailView
 
urlpatterns = patterns('',
    url(r'^(?P<feed>[-\w\d]+)/$', FeedTopArchiveView.as_view(), name='top_archive'),
    url(r'^(?P<feed>[-\w\d]+)/(?P<year>\d{4})/$', FeedYearArchiveView.as_view(), name='year_archive'),
    url(r'^(?P<feed>[-\w\d]+)/(?P<year>\d{4})/(?P<month>\w{3})/$', FeedMonthArchiveView.as_view(), name='month_archive'),
    url(r'^(?P<feed>[-\w\d]+)/(?P<year>\d{4})/(?P<month>\w{3})/(?P<day>\d{2})/(?P<slug>[-\w\d]+)/$', PostDetailView.as_view(), name='post_detail'),
)
