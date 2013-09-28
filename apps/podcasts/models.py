import datetime
import os

from django.db import models
from django.template.defaultfilters import slugify
from django.conf import settings
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from tinymce.models import HTMLField

def content_file_name(instance, filename):
    today = datetime.datetime.strftime(datetime.datetime.now(), '%Y/%m/%d')
    return '/'.join(['content', os.path.splitext(filename)[1][1:], today, filename])

class Podcast(models.Model):
    #Where I showed this skill
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, editable=False)
    #Synopsis of this place
    subtitle = models.CharField(max_length=250, editable=False)
    description = HTMLField()
    #What skill did I use here?
    logo = models.ImageField(upload_to=content_file_name, blank=True)
    itunes_link = models.URLField(blank=True)
    authors = models.ManyToManyField(User)

    class Meta:
        ordering = ['title']

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return ("episode_list", (), { 
                    "title" : self.slug,})

    def save(self, force_insert=False, force_update=False):
        self.slug = slugify(self.title)
        super(Podcast, self).save(force_insert, force_update)


class Episode(models.Model):
    #Title of the demonstration shown
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, editable=False)
    #Description of the item
    description = HTMLField()
    pub_date = models.DateTimeField(default=datetime.datetime.now)
    posted = models.DateTimeField(default=datetime.datetime.now, editable=False)
    #Where is this from
    podcast = models.ForeignKey(Podcast)
    #Where people can see done
    location = models.URLField(blank=True)
    #Sample to show
    file = models.FileField(upload_to=content_file_name, blank=True)

    class Meta:
        ordering = ['title']

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return ("episode_detail", (), { 
                    "title" : self.podcast.slug,
                    "slug" : self.slug,})

    def save(self, force_insert=False, force_update=False):
        self.slug = slugify(self.title)
        super(Episode, self).save(force_insert, force_update)

    
