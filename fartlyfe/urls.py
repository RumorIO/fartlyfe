import photologue
from tastypie.api import Api

from apps.feeds.views import FrontPageView
from fartlyfe.api.resources import EventResource, BlogResource
from feeds import RssBlogFeed, AtomBlogFeed, RssPodcastFeed, AtomPodcastFeed, iTunesPodcastsFeed

from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView

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
    
    url(r'^$', FrontPageView.as_view(), name="front"),
    url(r'^photologue/', include('photologue.urls')),
    url(r'^blogs/', include('apps.feeds.urls.blogs')),
    url(r'^podcasts/', include('apps.feeds.urls.podcasts')),
    url(r'^calendar/', include('apps.local_calendar.urls')),
    url(r'^shop/', include('shop.urls')),
    
    url(r'^topic/', include('apps.feeds.urls.topics')),
    url(r'^tags/', include('apps.feeds.urls.tags')), 
    url(r'^search/$', include('apps.search.urls')),
    url(r'^api/', include(fartlyfe_v1.urls)),
    
    url(r'^feeds/all/(?P<slug>[-\w]+)/rss.xml$', RssBlogFeed(), name="feed-rss"),
    url(r'^feeds/all/(?P<slug>[-\w]+)/atom.xml$', AtomBlogFeed(), name="feed-atom"),
    url(r'^feeds/podcast/(?P<slug>[-\w]+)/rss.xml$', RssPodcastFeed(), name="podcast-rss"),
    url(r'^feeds/podcast/(?P<slug>[-\w]+)/atom.xml$', AtomPodcastFeed(), name="podcast-atom"),
    url(r'^feeds/podcasts/(?P<slug>[-\w]+)/podcast.xml$', iTunesPodcastsFeed(), name="podcast-itunes"),
    
    url(r'^(?P<url>.*/)$', include('django.contrib.flatpages.urls')),

)
