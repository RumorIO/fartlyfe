from django.conf.urls.defaults import *

from tagging.models import Tag

from apps.feeds.views import TagListView, TagDetailView

urlpatterns = patterns('',
    url('^$', TagListView.as_view(
                queryset=Tag.objects.all(),
                template_name='feeds/tag_list.html'), 
                name='all_tags'),
    url('^(?P<id>[0-9]+)$', TagDetailView.as_view(
                template_name='feeds/tag_detail.html'),
                name='tag_detail'),

)
