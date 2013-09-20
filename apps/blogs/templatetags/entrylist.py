from django import template
from django.template.loader import render_to_string


def do_list_entries(parser, token):
    bits = token.contents.split()
    if len(bits) != 3:
        raise template.TemplateSyntaxError("%s tag takes 1 arguments" % bits[0])

    return ListEntriesNode(bits[2])

class ListEntriesNode(template.Node):
    def __init__(self, incoming_list_name):
        self.incoming_list_name = template.Variable(incoming_list_name)

    def render(self, context):
        try:
            incoming = self.incoming_list_name.resolve(context)
        except template.VariableDoesNotExist:
            return ''
        return render_to_string('blog/show_entries.html', { 'entry_list':  incoming })

register = template.Library()
register.tag('list_entries', do_list_entries)

