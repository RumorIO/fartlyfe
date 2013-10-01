from django.contrib import admin
from apps.podcasts.models import Podcast, Episode
from tinymce.models import HTMLField
from tinymce.widgets import TinyMCE


class PodcastAdmin(admin.ModelAdmin):
    pass

class EpisodeAdmin(admin.ModelAdmin):
    formfield_overrides = {
        HTMLField: {'widget': TinyMCE(
            attrs={'cols':50, 'rows':30},
            mce_attrs={'width':"560px"}
            )}
    }
    list_filter = ('status',)

    def queryset(self, request):
        qs = Episode.objects.all()
        if request.user.has_perm('podcasts.can_publish_episode'):
            return qs
        return qs.filter(podcast__authors=request.user)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'podcast':
            if not request.user.has_perm('podcasts.can_publish_episode'):
                kwargs['queryset'] = Podcast.objects.filter(authors=request.user)
        return super(EpisodeAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def formfield_for_choice_field(self, db_field, request, **kwargs):
        if db_field.name == 'status':
            LIVE_STATUS = 1
            SUBMITTED_STATUS = 2
            DRAFT_STATUS = 3
            if request.user.has_perm('podcasts.can_publish_episode'):
                kwargs['choices'] = (
                        (LIVE_STATUS, 'Live'),
                        (SUBMITTED_STATUS, 'Submitted'),
                        (DRAFT_STATUS, 'Draft'),)
            else:
                kwargs['choices'] = (
                        (SUBMITTED_STATUS, 'Submitted'),
                        (DRAFT_STATUS, 'Draft'),)
        return super(EpisodeAdmin, self).formfield_for_choice_field(db_field, request, **kwargs)

admin.site.register(Podcast, PodcastAdmin)
admin.site.register(Episode, EpisodeAdmin)

