from django.conf.urls import patterns, include, url

from endless_pagination.views import AjaxListView

from apps.feeds.models import Topic
from apps.feeds.views import TopicListView, TopicDetailView

urlpatterns = patterns('',
    url(r'^$', TopicListView.as_view(), name='all_topics'),
    url(r'^(?P<id>[0-9]+)/$', TopicDetailView.as_view(), name='posts_by_topic'),
)
