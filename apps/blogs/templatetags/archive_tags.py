from django import template
from django.template.loader import render_to_string

from apps.blogs.models import Entry

def do_archive_list(parser, token):
    bits = token.contents.split()
    if len(bits) != 1:
        raise template.TemplateSyntaxError("%s tag takes 0 arguments" % bits[0])
    return ArchiveListNode()

class ArchiveListNode(template.Node):
    def render(self, context):
        months = Entry.live.dates('pub_date', 'month', order='DESC') 
        return render_to_string('blog/archive_bar.html', { 'months':  months })

register = template.Library()
register.tag('archive_list', do_archive_list)

