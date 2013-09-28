from django.shortcuts import render_to_response
from django.views.generic import ListView, DetailView
from django.core.urlresolvers import reverse

from apps.podcasts.models import Episode, Podcast
from apps.podcasts.settings import SKILL_CHOICES


class PodcastListView(ListView):
    queryset = Podcast.objects.all()
    paginate_by = 10
    template_name = 'top_list.html'
    context_object_name = 'items'
    
    def get_context_data(self, **kwargs):
        context = super(PodcastListView, self).get_context_data( **kwargs)
        context['item_type']= 'podcast'
        return context

class EpisodeListView(ListView):
    template_name = 'podcasts/episodes_list.html'
    context_object_name = 'episodes'

    def get_queryset(self):
        return Episode.objects.filter(podcast__slug=self.kwargs['title'])

    def get_context_data(self, **kwargs):
        context = super(EpisodeListView, self).get_context_data( **kwargs)
        context['podcast']= Podcast.objects.get(slug=self.kwargs['title'])
        return context

class EpisodeDetailView(DetailView):
    template_name = 'podcasts/episode_detail.html'
    context_objects_name = 'episode'
    model = Episode

