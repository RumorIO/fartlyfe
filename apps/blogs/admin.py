from django.contrib import admin
from apps.blogs.models import Category, Entry, Blog
from tinymce.models import HTMLField
from tinymce.widgets import TinyMCE

class BlogAdmin(admin.ModelAdmin):
    pass

class CategoryAdmin(admin.ModelAdmin):
    pass

class EntryAdmin(admin.ModelAdmin):
    formfield_overrides = {
        HTMLField: {'widget': TinyMCE(
            attrs={'cols':50, 'rows':30},
            mce_attrs={'width':"560px"}
            )}
    }

    def queryset(self, request):
        return Entry.objects.all()

admin.site.register(Blog, BlogAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Entry, EntryAdmin)
