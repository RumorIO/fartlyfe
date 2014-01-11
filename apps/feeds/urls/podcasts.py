from django.conf.urls import patterns, include, url
from django.views.generic import ListView, DetailView

from apps.feeds.views import PodcastListView, PostListView, PostDetailView

urlpatterns = patterns('',

    url('^$', PodcastListView.as_view(), name='podcast_list'),
    url('^(?P<slug>[-\w0-9]+)/$', PostListView.as_view(), name='episode_list'),
    url(r'^archive/', include('apps.feeds.urls.archives')), 
 
)


