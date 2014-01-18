from django.shortcuts import render_to_response, get_object_or_404
from django.core.urlresolvers import reverse
from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.dates import YearArchiveView, MonthArchiveView, ArchiveIndexView
from django.db.models import Q, Max

from endless_pagination.views import AjaxListView
from tagging.models import Tag

from apps.feeds.models import Topic, Post, Feed
from apps.podcasts.settings import SKILL_CHOICES

class FrontPageView(AjaxListView):
    """Lists the front pages featured stories"""
    model = Feed
    template_name = 'feeds/front.html'
    page_template = 'feeds/front_page.html'
    paginate_by = 3
    queryset = Feed.published.annotate(Max("post__pub_date")).order_by('-post__pub_date__max')
    
    def get_context_data(self, **kwargs):
        context = super(FrontPageView, self).get_context_data( **kwargs)
        context['cover'] = Post.live.filter(featured=True).order_by('-pub_date')[0]
        context['featured'] = Post.live.filter(featured=True).order_by('-pub_date')[1:5]
        context['recent_posts'] = Post.live.filter(mimetype="").order_by('-pub_date')[:4]
        context['recent_podcasts'] = Post.live.filter(mimetype__icontains="audio").order_by('-pub_date')[:4]
        return context


class PostsByFeedView(AjaxListView):
    model = Post
    template_name = 'feeds/post_list.html'
    page_template = 'feeds/post_list_page.html'

    def get_queryset(self):
        return Post.live.filter(feed__slug=self.kwargs['slug'])

    def get_context_data(self, **kwargs):
        context = super(PostsByFeedView, self).get_context_data( **kwargs)
        context['feed'] = Feed.published.get(slug=self.kwargs['slug'])
        return context


class FeedTopArchiveView(TemplateView):
    """Lists all years with posts"""
    template_name = 'feeds/year_list.html'
    
    def get_context_data(self, **kwargs):
        context = super(FeedTopArchiveView, self).get_context_data( **kwargs)
        yearmonths = {}
        for month in Post.live.filter(feed__slug=self.kwargs['slug']).dates('pub_date_year', 'month', order='ASC'):
            if yearmonths.has_key(month.year):
                if month not in yearmonths[month.year]:
                    yearmonths[month.year].append(month)
            else:
                yearmonths[month.year] = [month,]
        years_list = yearmonths.items()
        years_list.sort()
        context['years'] = years_list
        context['feed'] = Feed.published.get(slug=self.kwargs['slug'])
        return context


class FeedYearArchiveView(AjaxListView):
    """Lists all months in a given year that contain posts"""
    date_field='pub_date_year'
    template_name = 'feeds/post_archive_year.html'
    page_template = 'feeds/post_archive_year_page.html'

    def get_queryset(self):
        return Post.live.filter(feed__slug=self.kwargs['slug'])


class FeedMonthArchiveView(MonthArchiveView):
    """Lists all posts in a given month"""
    date_field = 'pub_date_year'
    template_name = ''

    def get_queryset(self):
        return Post.live.filter(feed__slug=self.kwargs['slug'])
 
    def get_context_data(self, **kwargs):
        context = super(FeedMonthArchiveView, self).get_context_data( **kwargs)
        context['feed'] = Feed.published.get(slug=self.kwargs['slug'])
        return context

class PostDetailView(DetailView):
    """Displays a page for any given post"""
    date_filed = 'pub_date'
    template_name = 'feeds/post_detail.html'
    
    def get_queryset(self):
        return Post.live.filter(feed__slug=self.kwargs['feed'])

        
class TopicDetailView(AjaxListView):
    """Displays all posts under a given topic"""
    model = Topic
    template_name = 'feeds/topic_list.html'
    context_object_name = 'entries'

    def get_queryset(self):
        return Post.live.filter(categories__slug=self.kwargs['slug'])

    def get_context_data(self, **kwargs):
        context = super(ByTopicView, self).get_context_data( **kwargs)
        context['topic']= get_object_or_404(Topic, slug=self.kwargs['slug'])
        return context


class TopicListView(AjaxListView):
    """Lists all topics"""
    model = Topic
    queryset = Topic.objects.all()
    template_name = 'feeds/categories.html'


class TagDetailView(DetailView):
    """Lists all posts with given tag"""

    def get_queryset(self):
        return Post.live.filter(tag=Tag.objects.get(id=self.kwargs['id']))


class TagListView(AjaxListView):
    """Lists all tags"""
    queryset = Tag.objects.all()
    
    def get_context_data(self, **kwargs):
        alphabet = map(chr, range(65, 91))
        alphabet_tag_list = [[letter, Post.live.filter(name__istartswith=letter)] for letter in alphabet]
        alphabet_tag_list.append(['#', Post.live.filter(name__iregex=r'^[^[:alpha:]]')])
        context = super(ByTopicView, self).get_context_data( **kwargs)
        context['tag_list']= alphabet_tag_list
        return context

