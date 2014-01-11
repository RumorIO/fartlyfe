from django.db import models
from django.template.defaultfilters import slugify
from django.utils.timezone import datetime, now, timedelta, utc
from django.db.models import Q
from django.core.urlresolvers import reverse
from localflavor.us.models import USStateField, PhoneNumberField

from calendarium.models import Event, Occurrence

from south.modelsinspector import add_introspection_rules 
add_introspection_rules([], ["^localflavor\.us\.models\.USStateField"])
add_introspection_rules([], ["^localflavor\.us\.models\.PhoneNumberField"])


class Location(models.Model):

    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    website = models.URLField(blank=True)
    phone_number = PhoneNumberField()    
    street_address = models.CharField(max_length=250,)
    city = models.CharField(max_length=250,)
    state = USStateField()
    zipcode = models.CharField(max_length=5,)

    latitude = models.FloatField(blank=True, null=True, editable=False)
    longitude = models.FloatField(blank=True, null=True, editable=False)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return '/events/locations/'+self.slug

    def save(self):
        self.slug = slugify(self.name)
        from geopy import geocoders
        google = geocoders.GoogleV3()
        address, (self.latitude, self.longitude) = google.geocode(' '.join([self.street_address, self.city, self.state, self.zipcode]))
        if address:
            self.street_address, self.city, state_zip, country = address.split(',')
            self.city = self.city[1:]
            waste, self.state, self.zipcode = state_zip.split(' ')
        super(Location, self).save()

    def get_full_address(self):
        address = [self.street_address, self.city + ', ' + self.state + ' ' + self.zipcode]
        return address


class EventModelManager(models.Manager):
    """Custom manager for the ``Event`` model class."""
    def get_occurrences(self, start, end, category=None):
        """Returns a list of events and occurrences for the given period."""
        # we always want the time of start and end to be at 00:00
        start = start.replace(minute=0, hour=0)
        end = end.replace(minute=0, hour=0)
        # if we recieve the date of one day as start and end, we need to set
        # end one day forward
        if start == end:
            end = start + timedelta(days=1)

        # retrieving relevant events
        # TODO currently for events with a rule, I can't properly find out when
        # the last occurrence of the event ends, or find a way to filter that,
        # so I'm still fetching **all** events before this period, that have a
        # end_recurring_period.
        # For events without a rule, I fetch only the relevant ones.
        qs = self.get_query_set()
        if category:
            qs = qs.filter(start__lt=end)
            relevant_events = qs.filter(
                Q(category=category) |
                Q(category__parent=category)
            )
        else:
            relevant_events = qs.filter(start__lt=end)
        # get all occurrences for those events that don't already have a
        # persistent match and that lie in this period.
        all_occurrences = []
        for event in relevant_events:
            all_occurrences.extend(event.get_occurrences(start, end))

        # sort and return
        return sorted(all_occurrences, key=lambda x: x.start)


class LocalEvent(Event):

    AGE_LIMITS = (
        (1, 'All Ages'),
        (2, '18+'),
        (3, '21+'),
        )

    approved = models.BooleanField()
    location = models.ForeignKey(Location, blank=True, null=True)
    age_limit = models.IntegerField(choices=AGE_LIMITS)
    price = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    fartlyfe_official = models.BooleanField()

    objects = EventModelManager()

    def save(self):
        if self.price == None:
            self.price = 0.00
        return super(LocalEvent, self).save()

    def get_absolute_url(self):
        return reverse('calendar_event_detail', kwargs={'pk': self.pk,})

class LocalOccurrence(Occurrence):

    LocalEvent = models.ForeignKey(LocalEvent, related_name='local_occurrences',)
    
    def get_absolute_url(self):
        return reverse('calendar_occurrence_detail', kwargs={
            'pk': self.pk,
            'year': self.start.year,
            'month': self.start.month,
            'day': self.start.day,
            })



