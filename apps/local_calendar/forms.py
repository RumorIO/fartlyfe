from django import forms
from datetimewidget.widgets import DateTimeWidget

from apps.local_calendar.models import LocalEvent



class LocalEventForm(forms.ModelForm):

    class Meta:
        model=LocalEvent
        exclude = ['created_by', 'approved', 'fartlyfe_official','image',]
        dateTimeOptions = {
            'format': 'dd/mm/yyyy HH:ii P',
            'autoclose': 'true',
            'showMeridian' : 'true'
            }

        widgets = {
                #Use localization
                'start': DateTimeWidget(options = dateTimeOptions, attrs={'id':"id_start_widget"},),
                'end': DateTimeWidget(options = dateTimeOptions, attrs={'id':"id_end"},),
            }

