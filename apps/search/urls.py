from django.conf.urls import patterns, include, url

from apps.search.views import search

urlpatterns = patterns('',
    url(r'^$', 'apps.search.views.search', name='search_results'),
)
