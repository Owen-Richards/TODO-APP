from datetime import datetime, timedelta, date
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.views import generic
from django.utils.safestring import mark_safe
from django.shortcuts import get_list_or_404, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import *
from .utils import Calendar
from .forms import EventForm
import calendar
from django.contrib.auth.decorators import login_required

def index(request):
    return HttpResponse('hello')

# calendar view
# https://www.huiwenteo.com/normal/2018/07/24/django-calendar.html
class CalendarView(LoginRequiredMixin, generic.ListView):
    model = Event
    template_name = 'cal/calendar.html'
    redirect_field_name = '/'
    login_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # use today's date for the calendar
        d = get_date(self.request.GET.get('month', None))

        # Instantiate our calendar class with today's year and date
        cal = Calendar(d.year, d.month)

        # Call the formatmonth method, which returns our calendar as a table
        html_cal = cal.formatmonth(self.request.user, withyear=True)
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        return context
    def get_queryset(self):
        return Event.objects.filter(author=self.request.user)

# get_date, prev_month, next_month
# https://www.huiwenteo.com/normal/2018/07/29/django-calendar-ii.html
def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split('-'))
        return date(year, month, day=1)
    return datetime.today()

def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month

def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month  

@login_required(login_url='/')
def event(request, event_id=None):
    if(request.method=='POST'):
        data=request.POST

        event = Event.objects.create(
            title=data['title'],
            description=data['description'],
            start_time=data['starttime'],
            end_time=data['endtime'],
            author=request.user,
            start_time_string=data['starttime'],
            end_time_string=data['endtime'],
        )

        return redirect('oauth_app:calendar')

    return render(request, 'cal/event.html')  

@login_required(login_url='/')
def editEvent(request, event_id=None):
    currEvent=Event.objects.get(pk=event_id)
    if(request.POST): 
        data=request.POST
        Event.objects.filter(pk=event_id).update(
            title=data['title'],
            description=data['description'],
            start_time=data['starttime'],
            end_time=data['endtime'],
            author=request.user,
            start_time_string=data['starttime'],
            end_time_string=data['endtime']
            )
        return redirect('oauth_app:calendar')
    return render(request, 'cal/edit.html', {'event': currEvent})
    
def delete_event(request, event_id):
    event=Event.objects.filter(pk=event_id)
    event.delete()
    return redirect('oauth_app:calendar')
    
@login_required(login_url='/')
def allTasks(request):
    t=datetime.now()
    eventList = Event.objects.filter(start_time__lte=t,end_time__gte=t,author=request.user)
    return render(request, 'cal/taskList.html', {'eventList': eventList})
@login_required(login_url='/')
def editTask(request, event_id=None):
    currEvent=Event.objects.get(pk=event_id)
    if(request.POST): 
        data=request.POST
        Event.objects.filter(pk=event_id).update(
            title=data['title'],
            description=data['description'],
            start_time=data['starttime'],
            end_time=data['endtime'],
            author=request.user,
            start_time_string=data['starttime'],
            end_time_string=data['endtime']
            )
        return redirect('oauth_app:task-list')
    return render(request, 'cal/editTask.html', {'event': currEvent})
def delete_task(request, event_id):
    event=Event.objects.filter(pk=event_id)
    event.delete()
    return redirect('oauth_app:task-list')
