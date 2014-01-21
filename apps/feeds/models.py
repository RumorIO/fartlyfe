import datetime
import os
import audioread

from django.db import models
from django.db.models import Q
from django.template.defaultfilters import slugify
from django.conf import settings
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from tinymce.models import HTMLField
from photologue.models import Gallery, Photo
from tagging.fields import TagField
from tagging.managers import ModelTagManager, ModelTaggedItemManager


def content_file_name(instance, filename):
    today = datetime.datetime.strftime(datetime.datetime.now(), '%Y/%m/%d')
    return '/'.join(['content', os.path.splitext(filename)[1][1:], today, filename])


class PublicFeedManager(models.Manager):
    def get_queryset(self):
        return super(PublicFeedManager,self).get_query_set().filter(public=True)
 

class Feed(models.Model):
    
    objects = models.Manager()
    published = PublicFeedManager()
    
    title = models.CharField(max_length=250, help_text='Maximum 250 characters.')
    slug = models.SlugField(unique=True, help_text="Automatically comes from title. Must be unique.", blank=True, editable=False)
    description = HTMLField()
    image = models.ForeignKey(Photo, blank=True, null=True, on_delete=models.SET_NULL)
    authors = models.ManyToManyField(User)
    public = models.BooleanField()

    #Podcast Info
    is_audio_podcast = models.BooleanField()
    is_video_podcast = models.BooleanField()
    copyright = models.CharField(max_length=250, blank=True, editable=False)
    summary = models.CharField(max_length=250, blank=True, editable=False)
    explicit = models.BooleanField()
    itunes_link = models.URLField(max_length=250, blank=True)
    copyright = models.CharField(max_length=250, blank=True)
    block = models.BooleanField()
    complete = models.BooleanField()

    class Meta:
        ordering = ['title']

    def save(self):
        self.slug = slugify(self.title)
        super(Feed, self).save()

    def __unicode__(self):
        return unicode(self.title)

    @models.permalink
    def get_absolute_url(self):
        return ('posts_by_feed', (), {'slug': self.slug })

    def live_entry_set(self):
        from apps.feeds.models import Post
        return self.entry_set.filter(status=Post.LIVE_STATUS)


class Topic(models.Model):

    title = models.CharField(max_length=250, help_text='Maximum 250 characters.')
    slug = models.SlugField(unique=True, help_text="Automatically comes from title. Must be unique.", blank=True, editable=False)
    description = HTMLField()
    image = models.ForeignKey(Photo, blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        ordering = ['title']

    def save(self):
        self.slug = slugify(self.title)
        super(Topic, self).save()

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return ('topic_detail', (), {'slug': self.slug })
    
    def live_entry_set(self):
        from apps.feeds.models import Post
        return self.entry_set.filter(status=Post.LIVE_STATUS)


class LivePostManager(models.Manager):
    def get_query_set(self):
        return super(LivePostManager,self).get_query_set().filter(Q(status=self.model.LIVE_STATUS),Q(pub_date__lte=datetime.datetime.now()),Q(feed__public=True))


class Post(models.Model):
    LIVE_STATUS = 1
    SUBMITTED_STATUS = 2
    DRAFT_STATUS = 3
    STATUS_CHOICES = (
        (LIVE_STATUS, 'Live'),
        (SUBMITTED_STATUS, 'Submitted'),
        (DRAFT_STATUS, 'Draft'),)

    
    live = LivePostManager()
    objects = models.Manager()
    tags = ModelTagManager()
    tagged = ModelTaggedItemManager()

    feed = models.ForeignKey(Feed)
    status = models.IntegerField(choices=STATUS_CHOICES, default=LIVE_STATUS)
    title = models.CharField(max_length=250)
    body = HTMLField()
    summary = models.CharField(max_length=250)
    pub_date = models.DateTimeField(default=datetime.datetime.now)
    pub_date_year = models.DateField(editable=False)
    posted = models.DateTimeField(default=datetime.datetime.now, editable=False)
    slug = models.SlugField(unique_for_date='pub_date', blank=True, editable=False)
    topics = models.ManyToManyField(Topic, blank=True)
    cover = models.ForeignKey(Photo)
    gallery = models.ForeignKey(Gallery, blank=True, null=True, default=None)
    tags = TagField(help_text="Seperate with spaces. Put multi-word tags in quotes.", verbose_name='tags')
    featured = models.BooleanField()

    #Media
    media = models.FileField(upload_to=content_file_name, blank=True, null=True)

    #Podcast-specific info
    explicit = models.BooleanField()
    description = models.CharField(max_length=250, blank=True)
    mimetype = models.CharField(max_length=250, blank=True, editable=False)
    duration = models.CharField(max_length=250, blank=True, editable=False)
    block = models.BooleanField()

    class Meta:
        ordering = ['-pub_date']
        permissions = (('can_publish_entry', 'Can publish entry'), ('can_publish_front', 'Can post on front page'))
    
    def save(self):
        self.pub_date_year = self.pub_date.date()
        self.slug = slugify(self.title)
        if len(self.slug) > 50:
            self.slug = self.slug[:49]
        if self.media:
            import mimetypes
            self.mimetype = mimetypes.guess_type(self.media.name)
        if 'audio' in self.mimetype:
            import audioread
            self.duration = int(audioread.audio_open(self.media.path).duration)
        elif 'video' in self.mimetype:
            process = subprocess.Popen(['/usr/bin/ffmpeg', '-i', self.media.path], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            stdout, stderr = process.communicate()
            matches = re.search(r"Duration:\s{1}(?P\d+?):(?P\d+?):(?P\d+\.\d+?),", stdout, re.DOTALL).groupdict()
 
            hours = Decimal(matches['hours'])
            minutes = Decimal(matches['minutes'])
            seconds = Decimal(matches['seconds'])
 
            total = 0
            total += 60 * 60 * hours
            total += 60 * minutes
            total += seconds 
            self.duration = total
        return super(Post, self).save()

    def __unicode__(self):
        return unicode(self.title)

    @models.permalink
    def get_absolute_url(self):
        return ('post_detail', (), { 'feed': self.feed.slug,
                                        'year': self.pub_date.strftime("%Y"),
                                        'month': self.pub_date.strftime("%b").lower(),
                                        'day': self.pub_date.strftime("%d"),
                                        'slug': self.slug })

