from django.conf.urls import url
from django.urls import path, include
from . import views
from django.contrib.auth.decorators import login_required

app_name = 'oauth_app'
urlpatterns = [
    # url(r'^index/$', views.index, name='index'),
    # url(r'^calendar/$', views.CalendarView.as_view(), name='calendar'),
    # url(r'^calendar/event/new/$', views.event, name='event_new'),
    # url(r'^event/edit/(?P<event_id>\d+)/$', views.event, name='event_edit'), 
    path('index/', views.index, name='index'),
    path('calendar/', login_required(views.CalendarView.as_view(), login_url='/'), name='calendar'),
    path('calendar/month=<str:year>-<str:month>/', login_required(views.CalendarView.as_view(), login_url='/'), name='calendarPrevMonth'),
    path('calendar/event/new/', views.event, name='event_new'),
    path('event/edit/<int:event_id>/', views.editEvent, name='event_edit'),
    path('delete/<int:event_id>', views.delete_event, name='event_delete'),
    path('tasks/', views.allTasks, name='task-list'),
    path('tasks/event/new', views.event, name='task-addevent'),
    path('edit/tasks/<int:event_id>', views.editTask, name='edit-task'),
    path('deleteTask/<int:event_id>/', views.delete_task, name='delete-task')
]
