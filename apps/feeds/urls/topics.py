from django.conf.urls import patterns, include, url

from apps.feeds.models import Topic
from apps.feeds.views import AllTopicView, ByTopicView

urlpatterns = patterns('',
    url(r'^$', AllTopicView.as_view(), name='all_topics'),
    url(r'^(?P<id>[0-9]+)/$', ByTopicView.as_view(), name='posts_by_topic'),
)
