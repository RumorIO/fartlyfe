from django import template
from django.utils.safestring import mark_safe

from apps.myresume.models import ResumeItem
from apps.myresume.settings import MEDIA_EMBED_OPTION

register = template.Library()

@register.filter(name='embedding')
def embedding(value):
    result = ''
    resume_item = ResumeItem.objects.get(pk=value.pk)
    try:
        file_name = resume_item.file.url
    except ValueError:
        file_name = ''
    location_name = resume_item.location
    file_parts = file_name.split('.')
    location_parts = location_name.split('.')
    media_list = file_parts + location_parts
    for part in media_list:
        if part in MEDIA_EMBED_OPTION.keys():
            if part in file_parts:
                result = MEDIA_EMBED_OPTION[part] % file_name
            elif part in location_parts:
                if '?v=' in location_name:
                    location_name = location_name.split('?v=')[-1]
                result = MEDIA_EMBED_OPTION[part] % location_name
    return mark_safe(result)
