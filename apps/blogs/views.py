from django.shortcuts import render_to_response, get_object_or_404
from django.views.generic import ListView, DetailView
from django.views.generic.dates import YearArchiveView, MonthArchiveView, ArchiveIndexView

from apps.blogs.models import Category, Entry, Blog

class FrontPageView(ArchiveIndexView):
    template_name = 'blogs/entry_archive.html'
    context_object_name = 'latest'
    date_field = 'pub_date'
    paginate_by = 4
    queryset = Entry.live.filter(on_front=True)

class BlogListView(ListView):
    template_name = 'blogs/stream_list.html'
    context_object_name = 'items'
    queryset = Blog.objects.filter(public=True)
    
    def get_context_data(self, **kwargs):
        context = super(BlogListView, self).get_context_data( **kwargs)
        context['item_type']= 'blog'
        return context

class BlogPostListView(FrontPageView):
    
    def get_queryset(self):
        return Entry.live.filter(blog__slug=self.kwargs['blog'])
    
    def get_context_data(self, **kwargs):
        context = super(BlogPostListView, self).get_context_data( **kwargs)
        context['blog']= get_object_or_404(Blog, slug=self.kwargs['blog'])
        return context

class ByCategoryView(ListView):
    template_name = 'blogs/category_list.html'
    context_object_name = 'entries'

    def get_queryset(self):
        return Entry.live.filter(categories__slug=self.kwargs['slug'])

    def get_context_data(self, **kwargs):
        context = super(ByCategoryView, self).get_context_data( **kwargs)
        context['category']= get_object_or_404(Category, slug=self.kwargs['slug'])
        return context

class AllCategoryView(ListView):
    queryset = Category.objects.all()
    template_name = 'blogs/categories.html'
    context_object_name = 'categories'
 
class BlogTopArchiveView(ListView):
    template_name = 'blogs/entry_archive_top.html'
    context_object_name = 'years'

    def get_queryset(self):
        return Entry.live.dates('pub_date', 'year', order='DESC').filter(blog__slug=self.kwargs['blog'])

class BlogYearArchiveView(YearArchiveView):
    date_field='pub_date'
    template_name = 'blogs/entry_archive_year.html'

    def get_queryset(self):
        return Entry.live.filter(blog__slug=self.kwargs['blog'])

class BlogMonthArchiveView(MonthArchiveView):
    date_field='pub_date'
    template_name = 'blogs/entry_archive_month.html'

    def get_queryset(self):
        return Entry.live.filter(blog__slug=self.kwargs['blog'])

class BlogDetailView(DetailView):
    date_filed = 'pub_date'
    template_name = 'blogs/entry_detail.html'
    
    def get_queryset(self):
        return Entry.live.filter(blog__slug=self.kwargs['blog'])

        
class TagDetailView(DetailView):
    pass

class TagListView(ListView):
    pass




