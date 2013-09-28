from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Atom1Feed, Rss201rev2Feed
from django.shortcuts import get_object_or_404

from apps.blogs.models import Entry, Blog
from apps.podcasts.models import Episode, Podcast
import datetime
import audioread
import re

tags = re.compile('<.*?>')

class RssBlogFeed(Feed):
    
    def get_object(self, request, slug):
        return get_object_or_404(Blog, slug=slug)

    def title(self, obj):
        return obj.title

    def link(self, obj):
        return obj.get_absolute_url()

    def description(self, obj):
        return obj.description

    def items(self, obj):
        return Entry.live.filter(blog=obj)[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.body

class AtomBlogFeed(RssBlogFeed):
    feed_type = Atom1Feed
    subtitle = RssBlogFeed.description

class RssPodcastFeed(Feed):
    copyright = "&#x2117; &amp; &#xA9; 2013 fart lyfe"

    def get_object(self, request, slug):
        return get_object_or_404(Podcast, slug=slug)

    def title(self, obj):
        return obj.title

    def link(self, obj):
        return obj.get_absolute_url()

    def description(self, obj):
        import re
        tags = re.compile('<(.|\n)*?>')
        return tags.sub('', obj.description)
    
    def items(self, obj):
        return Episode.objects.filter(podcast=obj)

class AtomPodcastFeed(RssPodcastFeed):
    feed_type = Atom1Feed
    subtitle = RssPodcastFeed.description

class iTunesPodcastsFeedGenerator(Rss201rev2Feed):

    def rss_attributes(self):
        return {u"version": self._version, u"xmlns:atom": u"http://www.w3.org/2005/Atom", u'xmlns:itunes': u'http://www.itunes.com/dtds/podcast-1.0.dtd'}

    def add_root_elements(self, handler):
        super(iTunesPodcastsFeedGenerator, self).add_root_elements(handler)
        handler.addQuickElement(u'itunes:subtitle', self.feed['subtitle'])
        handler.addQuickElement(u'itunes:author', self.feed['author_name'])
        handler.addQuickElement(u'itunes:summary', self.feed['description'])
        handler.startElement(u"itunes:owner", {})
        handler.addQuickElement(u'itunes:name', self.feed['iTunes_name'])
        handler.addQuickElement(u'itunes:email', self.feed['iTunes_email'])
        handler.endElement(u'itunes:owner')
        handler.addQuickElement(u'itunes:image', attrs={'href':self.feed['iTunes_image_url']})
        handler.startElement(u"image", {})
        handler.addQuickElement(u"url", self.feed['iTunes_image_url'])
        handler.addQuickElement(u"title", self.feed["title"])
        handler.addQuickElement(u"link", self.feed["link"])
        handler.endElement(u"image") 
        handler.addQuickElement(u'itunes:category', attrs={'text':'Arts'})
         
    def add_item_elements(self,  handler, item):
        super(iTunesPodcastsFeedGenerator, self).add_item_elements(handler, item)
        handler.addQuickElement(u'itunes:summary', item['summary'])
        handler.addQuickElement(u'itunes:duration', item['duration'])

class iTunesPodcastPost():
    def __init__(self, podcast):
        self.id = podcast.id
        self.title = podcast.title
        self.summary = tags.sub('', podcast.description)
        self.enclosure_url = podcast.file.url
        self.enclosure_length = podcast.file.size
        self.enclosure_mime_type = u'audio/mpeg'
        self.duration = str(datetime.timedelta(seconds=int(audioread.audio_open(podcast.file.path).duration)))

    def __unicode__(self):
        return self.title
  
    def get_absolute_url(self):
        return self.enclosure_url

class iTunesPodcastsFeed(RssPodcastFeed):
    """
    A feed of podcasts for iTunes and other compatible podcatchers.
    """
    feed_type = iTunesPodcastsFeedGenerator
    feed_copyright = "Copyright 2013"
  
    def items(self, obj):
        """
        Returns a list of items to publish in this feed.
        """
        posts = super(iTunesPodcastsFeed, self).items(obj)
        posts = [iTunesPodcastPost(item) for item in posts]
        return posts

    def image_url(self, obj):
        if obj.logo:
            return obj.logo.url
        else:
            return ''

    def feed_extra_kwargs(self, obj):
        extra = {}
        author_name = str([author.get_full_name()+' ' for author in obj.authors.all()])
        subtitle = obj.subtitle
        summary = obj.description
        extra['iTunes_name'] = str([author.get_full_name() + ' ' for author in obj.authors.all()])
        extra['iTunes_email'] = str([author.email + ' ' for author in obj.authors.all()])
        extra['iTunes_image_url'] = self.image_url(obj)
        return extra

    def item_extra_kwargs(self, item):
        return {'summary':item.summary, 'duration':item.duration,}

    def item_enclosure_url(self, item):
        return item.enclosure_url
    
    def item_enclosure_length(self, item):
        return item.enclosure_length
    
    def item_enclosure_mime_type(self, item):
        return item.enclosure_mime_type

    def item_description(self, item):
        return item.summary
