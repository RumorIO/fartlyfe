from django.conf.urls.defaults import *

from apps.feeds.models import Post
from apps.feeds.views import StreamTopArchiveView, StreamYearArchiveView, StreamMonthArchiveView, PostDetailView
 
urlpatterns = patterns('',
    url(r'^(?P<feed>[-\w\d]+)/$', StreamTopArchiveView.as_view(), name='top_archive'),
    url(r'^(?P<feed>[-\w\d]+)/(?P<year>\d{4})/$', StreamYearArchiveView.as_view(), name='year_archive'),
    url(r'^(?P<feed>[-\w\d]+)/(?P<year>\d{4})/(?P<month>\w{3})/$', StreamMonthArchiveView.as_view(), name='month_archive'),
    url(r'^(?P<feed>[-\w\d]+)/(?P<year>\d{4})/(?P<month>\w{3})/(?P<day>\d{2})/(?P<slug>[-\w\d]+)/$', PostDetailView.as_view(), name='post_detail'),
)
