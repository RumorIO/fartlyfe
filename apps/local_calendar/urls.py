from django.conf.urls import patterns, include, url

from calendarium.views import (
    CalendariumRedirectView,
)

from apps.local_calendar.views import (
    LocalDayView,
    LocalWeekView,
    LocalMonthView,
    LocalEventDetailView,
    LocalEventCreateView,
    LocalOccurrenceDetailView,
    LocalUpcomingAjaxView,
    LocalCalendariumRedirectView,
)


urlpatterns = patterns(
    '',
    # event views
    url(r'^event/create/$',
        LocalEventCreateView.as_view(),
        name='calendar_event_create'),

    url(r'^event/(?P<pk>\d+)/$',
        LocalEventDetailView.as_view(),
        name='calendar_event_detail'),

    url(r'^once/(?P<pk>\d+)/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/$',
        LocalOccurrenceDetailView.as_view(),
        name='calendar_occurrence_detail'),

    # calendar views
    url(r'^(?P<year>\d+)/(?P<month>\d+)/$',
        LocalMonthView.as_view(),
        name='calendar_month'),

    url(r'^(?P<year>\d+)/week/(?P<week>\d+)/$',
        LocalWeekView.as_view(),
        name='calendar_week'),

    url(r'^(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/$',
        LocalDayView.as_view(),
        name='calendar_day'),

    url(r'^get-events/$',
        LocalUpcomingAjaxView.as_view(),
        name='calendar_upcoming_events'),

    url(r'^$',
        LocalCalendariumRedirectView.as_view(),
        name='calendar_main'),


)
