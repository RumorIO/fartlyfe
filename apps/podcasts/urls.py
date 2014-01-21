from django.conf.urls import patterns, include, url
from django.views.generic import ListView, DetailView

from apps.podcasts.views import PodcastListView, EpisodeListView, EpisodeDetailView

urlpatterns = patterns('',

    url('^$', PodcastListView.as_view(), name='podcast_list'),
    url('^(?P<title>[-\w]+)/$', EpisodeListView.as_view(), name='episode_list'),
    url('^(?P<title>[-\w]+)/(?P<slug>[-\w]+)/$', EpisodeDetailView.as_view(), name='episode_detail'),
 
)


