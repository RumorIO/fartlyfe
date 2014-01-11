from django.conf.urls import patterns, include, url

from apps.blogs.models import Entry
from apps.blogs.views import BlogTopArchiveView, BlogYearArchiveView, BlogMonthArchiveView, BlogDetailView

urlpatterns = patterns('',
    url(r'^(?P<blog>[-\w\d]+)/$', BlogTopArchiveView.as_view(), name='top_archive'),
    url(r'^(?P<blog>[-\w\d]+)/(?P<year>\d{4})/$', BlogYearArchiveView.as_view(), name='year_archive'),
    url(r'^(?P<blog>[-\w\d]+)/(?P<year>\d{4})/(?P<month>\w{3})/$', BlogMonthArchiveView.as_view(), name='month_archive'),
    url(r'^(?P<blog>[-\w\d]+)/(?P<year>\d{4})/(?P<month>\w{3})/(?P<day>\d{2})/(?P<slug>[-\w\d]+)/$', BlogDetailView.as_view(), name='entry_archive'),
)
