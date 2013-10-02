from django.contrib import admin
from apps.blogs.models import Category, Entry, Blog, TopEntry
from tinymce.models import HTMLField
from tinymce.widgets import TinyMCE

class BlogAdmin(admin.ModelAdmin):

    def get_form(self, request, obj=None, **kwargs):
        self.exclude = []
        if not request.user.is_superuser:
            self.exclude.append('authors')
        return super(BlogAdmin, self).get_form(request, obj, **kwargs) 

    def queryset(self, request):
        qs = Blog.objects.all()
        if request.user.has_perm('blogs.can_add_blog'):
            return qs
        return qs.filter(authors=request.user)


class CategoryAdmin(admin.ModelAdmin):
    pass

class EntryAdmin(admin.ModelAdmin):
    formfield_overrides = {
        HTMLField: {'widget': TinyMCE(
            attrs={'cols':50, 'rows':30},
            mce_attrs={'width':"560px"}
            )}
    }
    list_filter = ('status',)

    def queryset(self, request):
        qs = Entry.objects.all()
        if request.user.has_perm('blogs.can_publish_entry'):
            return qs
        return qs.filter(blog__authors=request.user)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'blog':
            if not request.user.has_perm('blogs.can_publish_entry'):
                kwargs['queryset'] = Blog.objects.filter(authors=request.user)
        return super(EntryAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def formfield_for_choice_field(self, db_field, request, **kwargs):
        if db_field.name == 'status':
            LIVE_STATUS = 1
            SUBMITTED_STATUS = 2
            DRAFT_STATUS = 3
            if request.user.has_perm('blogs.can_publish_entry'):
                kwargs['choices'] = (
                        (LIVE_STATUS, 'Live'),
                        (SUBMITTED_STATUS, 'Submitted'),
                        (DRAFT_STATUS, 'Draft'),)
            else:
                kwargs['choices'] = (
                        (SUBMITTED_STATUS, 'Submitted'),
                        (DRAFT_STATUS, 'Draft'),)
        return super(EntryAdmin, self).formfield_for_choice_field(db_field, request, **kwargs)
                
class TopEntryAdmin(admin.ModelAdmin):
    pass

admin.site.register(Blog, BlogAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Entry, EntryAdmin)
admin.site.register(TopEntry, TopEntryAdmin)

