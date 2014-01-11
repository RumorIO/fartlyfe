from django.contrib import admin
from django.contrib.flatpages.admin import FlatpageForm, FlatPageAdmin
from django.contrib.flatpages.models import FlatPage
from tinymce.models import HTMLField
from tinymce.widgets import TinyMCE
               
from apps.local_calendar.models import LocalEvent, Location


class LocationAdmin(admin.ModelAdmin):
    
    prepopulated_fields = {"slug": ("name",)}
    
    formfield_overrides = {
        HTMLField: {'widget': TinyMCE(
            attrs={'cols':50, 'rows':30},
            mce_attrs={'width':"560px"}
            )}
    }


class LocalEventAdmin(admin.ModelAdmin):
    pass

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

admin.site.register(Location, LocationAdmin)
admin.site.register(LocalEvent, LocalEventAdmin)
admin.site.unregister(FlatPage)
admin.site.register(FlatPage, HTMLFlatPageAdmin)
