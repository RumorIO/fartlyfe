from django.shortcuts import render_to_response, get_object_or_404
from django.core.urlresolvers import reverse
from django.views.generic import ListView, DetailView
from django.views.generic.dates import YearArchiveView, MonthArchiveView, ArchiveIndexView
from django.db.models import Q

from tagging.models import Tag

from apps.feeds.models import Topic, Post, Stream
from apps.podcasts.settings import SKILL_CHOICES

class FrontPageView(ArchiveIndexView):
    """Lists the front pages featured stories"""
    template_name = 'feeds/post_list.html'
    date_field = 'pub_date'
    paginate_by = 4
    queryset = Post.live.filter(on_front=True)


class BlogListView(ListView):
    """Filters out podcast feeds, to list blogs"""
    template_name = 'feeds/feed_list.html'
    queryset = Stream.objects.filter(Q(is_audio_podcast=False)|Q(is_video_podcast=False)).filter(public=True)
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(BlogListView, self).get_context_data( **kwargs)
        context['item_type']= 'blog'
        return context


class PodcastListView(BlogListView):
    """Lists only feeds tagged as podcasts"""
    queryset = Stream.objects.filter(Q(is_audio_podcast=False)|Q(is_video_podcast=False)).filter(public=True)
    
    def get_context_data(self, **kwargs):
        context = super(PodcastListView, self).get_context_data( **kwargs)
        context['item_type']= 'podcast'
        return context


class PostListView(FrontPageView):
    """Lists most recent public posts on a given feed"""
    def get_queryset(self):
        return Post.live.filter(feed__slug=self.kwargs['feed'])
    
    def get_context_data(self, **kwargs):
        context = super(StreamPostListView, self).get_context_data( **kwargs)
        context['feed']= get_object_or_404(Stream, slug=self.kwargs['feed'])
        return context


class PostDetailView(DetailView):
    """Displays a page for any given post"""
    date_filed = 'pub_date'
    template_name = 'feeds/post_detail.html'
    
    def get_queryset(self):
        return Post.live.filter(feed__slug=self.kwargs['feed'])


class ByTopicView(ListView):
    """Displays all posts under a given topic"""
    template_name = 'feeds/topic_list.html'
    context_object_name = 'entries'

    def get_queryset(self):
        return Post.live.filter(categories__slug=self.kwargs['slug'])

    def get_context_data(self, **kwargs):
        context = super(ByTopicView, self).get_context_data( **kwargs)
        context['topic']= get_object_or_404(Topic, slug=self.kwargs['slug'])
        return context


class AllTopicView(ListView):
    """Lists all topics"""
    queryset = Topic.objects.all()
    template_name = 'feeds/categories.html'


class StreamTopArchiveView(ListView):
    """Lists all years with posts"""
    template_name = 'feeds/post_archive_top.html'

    def get_queryset(self):
        return Post.live.dates('pub_date', 'year', order='DESC').filter(feed__slug=self.kwargs['feed'])


class StreamYearArchiveView(YearArchiveView):
    """Lists all months in a given year that contain posts"""
    date_field='pub_date'
    template_name = 'feeds/post_archive_year.html'

    def get_queryset(self):
        return Post.live.filter(feed__slug=self.kwargs['feed'])


class StreamMonthArchiveView(MonthArchiveView):
    """Lists all posts in a given month"""
    date_field='pub_date'
    template_name = 'feeds/post_archive_month.html'

    def get_queryset(self):
        return Post.live.filter(feed__slug=self.kwargs['feed'])

        
class TagDetailView(DetailView):
    """Lists all posts with given tag"""

    def get_queryset(self):
        return Post.live.filter(tag=Tag.objects.get(id=self.kwargs['id']))


class TagListView(ListView):
    """Lists all tags"""
    queryset = Tag.objects.all()
    
    def get_context_data(self, **kwargs):
        alphabet = map(chr, range(65, 91))
        alphabet_tag_list = [[letter, Business.objects.filter(name__istartswith=letter)] for letter in alphabet]
        alphabet_tag_list.append(['#', Business.objects.filter(name__iregex=r'^[^[:alpha:]]')])
        context = super(ByTopicView, self).get_context_data( **kwargs)
        context['tag_list']= alphabet_tag_list
        return context

