from django.conf.urls.defaults import *

from apps.blog.models import Entry
from apps.blog.views import BlogTopArchiveView, BlogYearArchiveView, BlogMonthArchiveView, BlogDetailView

urlpatterns = patterns('',
    url(r'^$', BlogTopArchiveView.as_view(), name='top_archive'),
    url(r'^(?P<year>\d{4})/$', BlogYearArchiveView.as_view(), name='year_archive'),
    url(r'^(?P<year>\d{4})/(?P<month>\w{3})/$', BlogMonthArchiveView.as_view(), name='month_archive'),
    url(r'^(?P<year>\d{4})/(?P<month>\w{3})/(?P<day>\d{2})/(?P<slug>[-\w]+)/$', BlogDetailView.as_view(), name='entry_archive'),
)
