from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView

from apps.feeds.views import FrontPageView
from apps.feeds.models import Post
from fartlyfe.api.resources import EventResource, BlogResource
from apps.feeds.feeds import iTunesPodcastsFeed

import photologue
from tastypie.api import Api
from endless_pagination.views import AjaxListView


from django.contrib import admin

fartlyfe_v1 = Api(api_name='fartlyfe_v1')
fartlyfe_v1.register(EventResource())
fartlyfe_v1.register(BlogResource())

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'fartlyfe.views.home', name='home'),
    # url(r'^fartlyfe/', include('fartlyfe.foo.urls')),
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    

    url(r'^$', FrontPageView.as_view(), name='main'),
    url(r'^featured/$', AjaxListView.as_view(
                            model = Post,
                            template_name='feeds/post_list.html',
                            page_template='feeds/post_list_page.html',
                            queryset=Post.live.filter(featured=True),), name='featured_posts'),
    
    url(r'^read/$', AjaxListView.as_view(
                            model = Post,
                            template_name='feeds/post_list.html',
                            page_template='feeds/post_list_page.html',
                            queryset=Post.live.filter(mimetype=''),), name='read_posts'),
    
    url(r'^listen/$', AjaxListView.as_view(
                            model = Post,
                            template_name='feeds/post_list.html',
                            page_template='feeds/post_list_page.html',
                            queryset=Post.live.filter(mimetype__icontains='audio'),), name='listen_posts'),
    
    
    url(r'^watch/$', AjaxListView.as_view(
                            model = Post,
                            template_name='feeds/post_list.html',
                            page_template='feeds/post_list_page.html',
                            queryset=Post.live.filter(mimetype__icontains='video'),), name='watch_posts'),
    
    
    url(r'^feeds/', include('apps.feeds.urls')),
    url(r'^calendar/', include('apps.local_calendar.urls')),
    url(r'^shop/', include('apps.this_shop.urls')),
    url(r'^topic/', include('apps.feeds.urls.topics')),
    url(r'^tags/', include('apps.feeds.urls.tags')), 
    

    url(r'^photologue/', include('photologue.urls')),
    url(r'^search/$', include('apps.search.urls')),
    url(r'^api/', include(fartlyfe_v1.urls)),
    
    
    url(r'^(?P<url>.*/)$', include('django.contrib.flatpages.urls')),

)


