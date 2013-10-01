import photologue

from apps.blogs.views import FrontPageView
from feeds import RssBlogFeed, AtomBlogFeed, RssPodcastFeed, AtomPodcastFeed, iTunesPodcastsFeed

from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

from django.contrib import admin
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
    url(r'^blogs/', include('apps.blogs.urls')),
    url(r'^podcasts/', include('apps.podcasts.urls')),
    #url(r'^calendar/', include('apps.calendar.urls')),
    #url(r'^studios/', include('apps.studios.urls')),
    url(r'^feeds/blog/(?P<slug>[-\w]+)/rss.xml$', RssBlogFeed(), name="blog-rss"),
    url(r'^feeds/blog/(?P<slug>[-\w]+)/atom.xml$', AtomBlogFeed(), name="blog-atom"),
    url(r'^feeds/podcast/(?P<slug>[-\w]+)/rss.xml$', RssPodcastFeed(), name="podcast-rss"),
    url(r'^feeds/podcast/(?P<slug>[-\w]+)/atom.xml$', AtomPodcastFeed(), name="podcast-atom"),
    url(r'^feeds/podcasts/(?P<slug>[-\w]+)/podcast.xml$', iTunesPodcastsFeed(), name="podcast-itunes"),
    url(r'^(?P<url>.*/)$', include('django.contrib.flatpages.urls')),

)
