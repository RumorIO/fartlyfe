from django.contrib import admin
from django.forms import ModelForm
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


class LocalEventAdminForm(ModelForm):
    class Meta:
        model = LocalEvent
        widgets = {
            'description' : TinyMCE(
                attrs={'cols':100, 'rows':30},
                mce_attrs={'width':'560px'})
            }

class LocalEventAdmin(admin.ModelAdmin):
    form = LocalEventAdminForm

admin.site.register(Location, LocationAdmin)
admin.site.register(LocalEvent, LocalEventAdmin)
    
    
