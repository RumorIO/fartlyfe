from django.shortcuts import render_to_response, get_object_or_404
from django.views.generic import ListView, DetailView
from django.views.generic.dates import YearArchiveView, MonthArchiveView, ArchiveIndexView

from apps.blog.models import Category, Entry

class BlogFrontView(ArchiveIndexView):
    template_name = 'blog/entry_archive.html'
    context_object_name = 'latest'
    date_field = 'pub_date'
    paginate_by = 4
    queryset = Entry.live.all()

class ByCategoryView(ListView):
    template_name = 'blog/category_list.html'
    context_object_name = 'entries'

    def get_queryset(self):
        return Entry.live.filter(categories__slug=self.kwargs['slug'])

    def get_context_data(self, **kwargs):
        context = super(ByCategoryView, self).get_context_data( **kwargs)
        context['category']= get_object_or_404(Category, slug=self.kwargs['slug'])
        return context

class AllCategoryView(ListView):
    queryset = Category.objects.all()
    template_name = 'blog/categories.html'
    context_object_name = 'categories'

class BlogTopArchiveView(ListView):
    queryset = Entry.live.dates('pub_date', 'year', order='DESC')
    template_name = 'blog/entry_archive_top.html'
    context_object_name = 'years'

class BlogYearArchiveView(YearArchiveView):
    queryset=Entry.live.all()
    date_field='pub_date'
    template_name = 'blog/entry_archive_year.html'

class BlogMonthArchiveView(MonthArchiveView):
    queryset=Entry.live.all()
    date_field='pub_date'
    template_name = 'blog/entry_archive_month.html'

class BlogDetailView(DetailView):
    queryset=Entry.live.all()
    date_filed = 'pub_date'
    template_name = 'blog/entry_detail.html'

def stop_errors(request):
    return HttpResponse("Go bot!")
