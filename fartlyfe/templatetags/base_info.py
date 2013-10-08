from django import template
from django.template.loader import render_to_string

import datetime

from apps.blogs.models import TopEntry, Entry
from apps.podcasts.models import Episode

def do_featured_entries(parser, token):
    bits = token.contents.split()
    if len(bits) != 1:
        raise template.TemplateSyntaxError("%s tag takes no arguments" % bits[0])
    return FeaturedEntriesNode()

class FeaturedEntriesNode(template.Node):

    def render(self, context):
        featured_entries = Entry.live.filter(featured=True)
        return render_to_string('blogs/featured_entries.html', { 'entries': featured_entries })

def do_recent_entries(parser, token):
    bits = token.contents.split()
    if len(bits) != 1:
        raise template.TemplateSyntaxError("%s tag takes no arguments" % bits[0])
    return RecentEntriesNode()

class RecentEntriesNode(template.Node):

    def render(self, context):
        recent_entries = Entry.live.order_by('-pub_date')[:5]
        return render_to_string('recent_list.html', { 'list': recent_entries })

def do_recent_episodes(parser, token):
    bits = token.contents.split()
    if len(bits) != 1:
        raise template.TemplateSyntaxError("%s tag takes no arguments" % bits[0])
    return RecentEpisodesNode()

class RecentEpisodesNode(template.Node):

    def render(self, context):
        recent_episodes = Episode.objects.filter(pub_date__lte=datetime.datetime.now()).order_by('-pub_date')[:5]
        return render_to_string('recent_list.html', { 'list': recent_episodes })


register = template.Library()
register.tag('featured_entries', do_featured_entries)
register.tag('recent_entries', do_recent_entries)
register.tag('recent_episodes', do_recent_episodes)

