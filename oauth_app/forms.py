from django.forms import ModelForm, DateInput
from .models import Event
from django.contrib.auth.models import User
from django.db import models
from django.db.models import CheckConstraint, Q, F
from django.core.exceptions import ValidationError

class EventForm(ModelForm):
  class Meta:
    
    model = Event
    # datetime-local is a HTML5 input type, format to make date time show on fields
    widgets = {
      'start_time': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
      'end_time': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
    }
    #fields = '__all__'
    fields = ['title', 'description', 'start_time', 'end_time']
    # https://stackoverflow.com/questions/2281179/adding-extra-constraints-into-fields-in-django
    # Used the link above for the constraints
    constraints = [
      CheckConstraint(
        check = Q(end_date__gt=F('start_date')), 
        name = 'check_start_date',
        ),
      ]

  def __init__(self, *args, **kwargs):
    super(EventForm, self).__init__(*args, **kwargs)
    # input_formats to parse HTML5 datetime-local input to datetime field
    self.fields['start_time'].input_formats = ('%Y-%m-%dT%H:%M',)
    self.fields['end_time'].input_formats = ('%Y-%m-%dT%H:%M',)
