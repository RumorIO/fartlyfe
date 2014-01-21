import datetime
from tinymce.models import HTMLField
from photologue.models import Gallery, Photo
from tagging.fields import TagField

from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify


class Blog(models.Model):
    
    title = models.CharField(max_length=250, help_text='Maximum 250 characters.')
    slug = models.SlugField(unique=True, help_text="Automatically comes from title. Must be unique.", blank=True, editable=False)
    description = HTMLField()
    authors = models.ManyToManyField(User)
    public = models.BooleanField()

    class Meta:
        ordering = ['title']
        permissions = (('can_edit_own_blog', 'Can edit own blog'),)

    def save(self):
        self.slug = slugify(self.title)
        super(Blog, self).save()

    def __unicode__(self):
        return unicode(self.title)

    def get_absolute_url(self):
        return "/blogs/%s/" %self.slug
    
    def live_entry_set(self):
        from apps.blogs.models import Entry
        return self.entry_set.filter(status=Entry.LIVE_STATUS)

class Category(models.Model):

    title = models.CharField(max_length=250, help_text='Maximum 250 characters.')
    slug = models.SlugField(unique=True, help_text="Automatically comes from title. Must be unique.", blank=True, editable=False)
    description = HTMLField()

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
        return super(LiveEntryManager,self).get_query_set().filter(status=self.model.LIVE_STATUS).filter(pub_date__lte=datetime.datetime.now()+datetime.timedelta(hours=1))
 
class Entry(models.Model):
    LIVE_STATUS = 1
    SUBMITTED_STATUS = 2
    DRAFT_STATUS = 3
    STATUS_CHOICES = (
        (LIVE_STATUS, 'Live'),
        (SUBMITTED_STATUS, 'Submitted'),
        (DRAFT_STATUS, 'Draft'),)

    
    live = LiveEntryManager()
    objects = models.Manager()
    
    blog = models.ForeignKey(Blog)
    status = models.IntegerField(choices=STATUS_CHOICES, default=LIVE_STATUS)
    title = models.CharField(max_length=250)
    body = HTMLField()
    summary = models.CharField(max_length=250)
    pub_date = models.DateTimeField(default=datetime.datetime.now)
    posted = models.DateTimeField(default=datetime.datetime.now, editable=False)
    slug = models.SlugField(unique_for_date='pub_date', editable=False, blank=True)
    categories = models.ManyToManyField(Category)
    cover = models.ForeignKey(Photo)
    gallery = models.ForeignKey(Gallery, blank=True, null=True, default=None)
    tags = TagField(help_text="Seperate with commas. Put mutli-word tags in quotes.", verbose_name='tags')
    on_front = models.BooleanField()
    featured = models.BooleanField()

    class Meta:
        verbose_name_plural = "Entries"
        ordering = ['-pub_date']
        permissions = (('can_publish_entry', 'Can publish entry'), ('can_publish_front', 'Can post on front page'))
    
    def save(self):
        self.slug = slugify(self.title)
        if len(self.slug) > 50:
            self.slug = self.slug[:49]
        super(Entry, self).save()

    def __unicode__(self):
        return unicode(self.title)
    
    @models.permalink
    def get_absolute_url(self):
        return ('entry_archive', (), { 'blog': self.blog.slug,
                                        'year': self.pub_date.strftime("%Y"),
                                        'month': self.pub_date.strftime("%b").lower(),
                                        'day': self.pub_date.strftime("%d"),
                                        'slug': self.slug })

