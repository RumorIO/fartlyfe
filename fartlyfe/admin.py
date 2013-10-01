from django.contrib.flatpages.admin import FlatpageForm, FlatPageAdmin
from django.contrib.flatpages.models import FlatPage
from django.contrib import admin
from tinymce.models import HTMLField
from tinymce.widgets import TinyMCE


class HTMLFlatPageForm(FlatpageForm):
    
    class Meta:
        model = FlatPage
        widgets = {
            'content' : TinyMCE(
                attrs={'cols':100, 'rows':30},
                mce_attrs={'width':'560px'})
            }

class HTMLFlatPageAdmin(FlatPageAdmin):
    form = HTMLFlatPageForm

admin.site.unregister(FlatPage)
admin.site.register(FlatPage, HTMLFlatPageAdmin)

