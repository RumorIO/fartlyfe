import datetime
from tinymce.models import HTMLField
from photologue.models import Gallery

from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

class Blog(models.Model):
    
    title = models.CharField(max_length=250, help_text='Maximum 250 characters.')
    slug = models.SlugField(unique=True, help_text="Automatically comes from title. Must be unique.", blank=True, editable=False)
    description = HTMLField()
    picture = models.ImageField(upload_to="media/blog/images/logos/", blank=True)
    author = models.ForeignKey(User)

    class Meta:
        ordering = ['title']

    def save(self):
        self.slug = slugify(self.title)
        super(Blog, self).save()

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return "/blogs/%s/" %self.slug
    
    def live_entry_set(self):
        from apps.blogs.models import Entry
        return self.entry_set.filter(status=Entry.LIVE_STATUS)



class Category(models.Model):

    title = models.CharField(max_length=250, help_text='Maximum 250 characters.')
    slug = models.SlugField(unique=True, help_text="Automatically comes from title. Must be unique.", blank=True, editable=False)
    description = HTMLField()
    picture = models.ImageField(upload_to="media/blog/images/categorylogos/", blank=True)

    class Meta:
        ordering = ['title']
        verbose_name_plural = "Categories"

    def save(self):
        self.slug = slugify(self.title)
        super(Category, self).save()

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return "/blog/category/%s/" %self.slug
    
    def live_entry_set(self):
        from apps.blogs.models import Entry
        return self.entry_set.filter(status=Entry.LIVE_STATUS)

class LiveEntryManager(models.Manager):
    def get_query_set(self):
        return super(LiveEntryManager,self).get_query_set().filter(status=self.model.LIVE_STATUS)

class Entry(models.Model):
    LIVE_STATUS = 1
    DRAFT_STATUS = 2
    STATUS_CHOICES = (
        (LIVE_STATUS, 'Live'),
        (DRAFT_STATUS, 'Draft'),)

    live = LiveEntryManager()
    objects = models.Manager()
    
    blog = models.ForeignKey(Blog)
    status = models.IntegerField(choices=STATUS_CHOICES, default=LIVE_STATUS)
    title = models.CharField(max_length=250)
    body = HTMLField()
    pub_date = models.DateTimeField(default=datetime.datetime.now)
    slug = models.SlugField(unique_for_date='pub_date', editable=False, blank=True)
    categories = models.ManyToManyField(Category)
    gallery = models.ForeignKey(Gallery, blank=True, null=True, default=None)


    def save(self):
        self.slug = slugify(self.title)
        if len(self.slug) > 50:
            self.slug = self.slug[:49]
        super(Entry, self).save()

    class Meta:
        verbose_name_plural = "Entries"
        ordering = ['-pub_date']

    def __unicode__(self):
        return self.title
    
    @models.permalink
    def get_absolute_url(self):
        return ('entry_archive', (), { 'year': self.pub_date.strftime("%Y"),
                                             'month': self.pub_date.strftime("%b").lower(),
                                             'day': self.pub_date.strftime("%d"),
                                             'slug': self.slug })

