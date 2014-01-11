from calendarium.views import MonthView, WeekView, DayView, EventDetailView, EventCreateView, OccurrenceDetailView, UpcomingEventsAjaxView 
from calendarium.utils import monday_of_week
from apps.local_calendar.models import LocalEvent, LocalOccurrence
from apps.local_calendar.forms import LocalEventForm

import calendar
from dateutil.relativedelta import relativedelta
from django.contrib.auth.models import User
from django.views.generic.edit import CreateView
from django.utils.timezone import datetime, now, timedelta, utc
from django.http import Http404, HttpResponseRedirect


class LocalMonthView(MonthView):
    template_name = 'calendar/month.html'

    def get_context_data(self, **kwargs):
        ctx = self.get_category_context()
        month = [[]]
        week = 0
        start = datetime(year=self.year, month=self.month, day=1, tzinfo=utc)
        end = datetime(
            year=self.year, month=self.month, day=1, tzinfo=utc
        ) + relativedelta(months=1)
        
        all_occurrences = LocalEvent.objects.get_occurrences( start, end, ctx.get('current_category'))
        for day in calendar.Calendar(firstweekday=6).itermonthdays(self.year, self.month):
            current = False
            if day:
                date = datetime(year=self.year, month=self.month, day=day,
                                tzinfo=utc)
                occurrences = filter(
                    lambda occ, date=date: occ.start.replace(
                        hour=0, minute=0, second=0, microsecond=0) == date,
                    all_occurrences)
                if date.date() == now().date():
                    current = True
            else:
                occurrences = []
            month[week].append((day, occurrences, current))
            if len(month[week]) == 7:
                month.append([])
                week += 1
        ctx.update({'month': month, 'date': date})
        return ctx 


class LocalWeekView(WeekView):
    template_name = 'calendar/week.html'

    def get_context_data(self, **kwargs):
        ctx = self.get_category_context()
        date = monday_of_week(self.year, self.week)+relativedelta(days=-1)
        week = []
        day = 0
        start = date
        end = date + relativedelta(days=7)
        all_occurrences = LocalEvent.objects.get_occurrences(
            start, end, ctx.get('current_category'))
        while day < 7:
            current = False
            occurrences = filter(
                lambda occ, date=date: occ.start.replace(
                    hour=0, minute=0, second=0, microsecond=0) == date,
                all_occurrences)
            if date.date() == now().date():
                current = True
            hours_list = []
            for occ in occurrences:
                hours_list.append({'event_time': occ.start.replace(minute=0, second=0), 'event_info': occ }) 
            hours_list.sort()
            date = date + timedelta(days=1)
            week.append((date, occurrences, hours_list, current))
            day += 1
        ctx.update({'week': week, 'date': date, 'week_nr': self.week})
        return ctx


class LocalDayView(DayView):
    template_name = 'calendar/day.html'

    def get_context_data(self, **kwargs):
        ctx = self.get_category_context()
        all_occurrences = LocalEvent.objects.get_occurrences(
            self.date, self.date, ctx.get('current_category'))
        occurrences = filter(
            lambda occ, date=self.date: occ.start.replace(
                hour=0, minute=0, second=0, microsecond=0) == date,
            all_occurrences)
        self.date = self.date + timedelta(days=1)
        ctx.update({'day': self.date, 'occurrences': occurrences})
        return ctx


class LocalEventCreateView(CreateView):
    template_name='calendar/event_create.html'
    model = LocalEvent
    form_class = LocalEventForm

    def get_initial(self):
        calendar_guest = User.objects.get(username='CalendarGuest')

        return {
            'created_by':calendar_guest,
            'approved':False,
            'fartlyfe_official':False,}


class LocalEventDetailView(EventDetailView):
    template_name = 'calendar/event_detail.html'


class LocalOccurrenceDetailView(OccurrenceDetailView):
    template_name = 'calendar/occurrence_detail.html'
    context_object_name = 'occurrence'

    def dispatch(self, request, *args, **kwargs):
        try:
            self.event = LocalEvent.objects.get(pk=kwargs.get('pk'))
        except LocalEvent.DoesNotExist:
            raise Http404
        year = int(kwargs.get('year'))
        month = int(kwargs.get('month'))
        day = int(kwargs.get('day'))
        try:
            date = datetime(year, month, day, tzinfo=utc)
        except (TypeError, ValueError):
            raise Http404
        # this should retrieve the one single occurrence, that has a
        # matching start date
        try:
            occ = LocalOccurrence.objects.get(
                start__year=year, start__month=month, start__day=day)
        except LocalOccurrence.DoesNotExist:
            occ_gen = self.event.get_occurrences(self.event.start)
            occ = occ_gen.next()
            while occ.start.date() < date.date():
                occ = occ_gen.next()
        if occ.start.date() == date.date():
            self.occurrence = occ
        else:
            raise Http404
        self.object = occ
        return super(LocalOccurrenceDetailView, self).dispatch(
            request, *args, **kwargs)


class LocalUpcomingAjaxView(UpcomingEventsAjaxView):
    pass

