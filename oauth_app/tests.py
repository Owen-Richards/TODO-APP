from django.test import TestCase
from django.contrib.auth.models import AnonymousUser, User
from django.test import RequestFactory, TestCase
from datetime import datetime, timedelta, date
from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.views import generic
from django.utils.safestring import mark_safe
from django.shortcuts import get_list_or_404, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.test import Client
from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from datetime import datetime, timedelta
from django.urls import reverse
from django.core import mail

from .models import *
from .utils import Calendar
from .forms import EventForm
import calendar
from django.test import TestCase
import pytz
import datetime

from django.test import TestCase
from django.utils import timezone

from .views import index, prev_month, get_date, allTasks, delete_event, event, next_month, CalendarView

# Login test cases
class LoginTest(TestCase):

    # setUp to create a login user
    def setUp(self):
        User = get_user_model()
        user = User.objects.create_user(username='Owen', email='olr7ms@virginia.edu')
        user.set_password('LetsTest')
        user.save()

    # Login with the correct user info
    def correct_user_info(self):
        c = Client()
        logged_in = c.login(username='Owen', password='LetsTest')
        self.assertTrue(logged_in)

    # Log Out with correct user info
    def logout_user(self):
        c = Client()
        c.login(username='Owen', password='LetsTest')
        User = get_user_model()
        user = User.objects.get(username='Owen')
        self.assertTrue(user.is_authenticated)
        c.logout()
        self.assertFalse(user.is_anonymous)

    # Trying to log in with the incorrect user
    def incorrect_username(self):
        c = Client()
        logged_in = c.login(username='Richards', password='LetsTest')
        self.assertFalse(logged_in)

    # Incorrect Password test
    def incorrect_password(self):
        c = Client()
        logged_in = c.login(username='Owen', password='Testing')
        self.assertFalse(logged_in)

    # Incorrect username and password trying to log in
    def incorrect_user(self):
        c = Client()
        logged_in = c.login(username='Richards', password='Testing')
        self.assertFalse(logged_in)

class RegisterTest(TestCase):
    # Test Login
    def normal_registration(self):
        c = Client(HTTP_HOST='example.com')
        response = c.post('/index/', {'username': 'owen', 'email': 'olr7ms@virginia.edu', 'password': 'Password!', 'second_password': 'Lewis'}, secure=True)
        logged_in = c.login(username='owen', password='Password!')
        self.assertFalse(logged_in)

    # Not correct password - non-Redirect
    def test_nonmatching_passwords(self):
        c = Client()
        response = c.post('/index/', {'username': 'owen', 'email': 'olr7ms@virginia.edu', 'password': 'Password!', 'second_password': 'hello'}, secure=True)
        self.assertEquals(response.status_code, 200)

    # Not correct email - non-Redirect
    def test_improper_email(self):
        c = Client()
        response = c.post('/index/', {'username': 'owen', 'email': 'owen@gmail.edu', 'password': 'Password!', 'second_password': 'Lewis'}, secure=True)
        self.assertEquals(response.status_code, 200)

# Testing Forms
# Testing Forms
class HomePageTest(TestCase):

    def test_forms(self):
        request = RequestFactory().get('index/')
        view = index(request)
        self.assertEquals(view.status_code,200)

    def test_forms1(self):
        request = RequestFactory().get('')
        view = index(request)
        self.assertEquals(view.status_code,200)

    def test_forms2(self):
        request = RequestFactory().get('calendar.html')
        view = index(request)
        self.assertEquals(view.status_code,200)
    
    def test_forms3(self):
        request = RequestFactory().get('delete.html')
        view = index(request)
        self.assertEquals(view.status_code,200)
    
    def test_forms4(self):
        request = RequestFactory().get('event.html')
        view = index(request)
        self.assertEquals(view.status_code,200)

    def test_forms5(self):
        request = RequestFactory().get('taskList.html')
        view = index(request)
        self.assertEquals(view.status_code,200)

    def test_forms6(self):
        request = RequestFactory().get('task/')
        view = index(request)
        self.assertEquals(view.status_code,200)

    def test_forms7(self):
        request = RequestFactory().get('event/')
        view = index(request)
        self.assertEquals(view.status_code,200)

    def test_forms8(self):
        request = RequestFactory().get('event/edit/<int:event_id>/')
        view = index(request)
        self.assertEquals(view.status_code,200)

    def test_forms9(self):
        request = RequestFactory().get('event/edit/<int:event_id>/delete.html')
        view = index(request)
        self.assertEquals(view.status_code,200)

    def test_forms10(self):
        request = RequestFactory().get('calendar/month=<str:year>-<str:month>/')
        view = index(request)
        self.assertEquals(view.status_code,200)

    def test_forms11(self):
        request = RequestFactory().get('base.html')
        view = index(request)
        self.assertEquals(view.status_code,200)

    # Failed test attempt
    # def previous_m(self):
    #     d = get_date('2021-10')
    #     month = prev_month(d)
    #     self.assertEquals('September', month)

# Anomynous person trying to access edit
class AnomEditTest(TestCase):
    def test_editEvent1(self):
        self.factory = RequestFactory()
        request=self.factory.get("/edit")
        request.user=AnonymousUser()
        response=event(request)
        self.assertEquals(response.status_code,302)

# Anomynous person trying to access event
class AnomEventTest(TestCase):       
    def test_eventEvent1(self):
        self.factory = RequestFactory()
        request=self.factory.get("/event")
        request.user=AnonymousUser()
        response=event(request)
        self.assertEquals(response.status_code,302)

# Anomynous person trying to access calendar/event/new
class AnomEventNewTest(TestCase):       
    def test_calendareventEvent1(self):
        self.factory = RequestFactory()
        request=self.factory.get("/calendar/event/new/")
        request.user=AnonymousUser()
        response=event(request)
        self.assertEquals(response.status_code,302)

# Anomynous person trying to access taskList
class AnomTaskTest(TestCase):       
    def test_tasklistEvent1(self):
        self.factory = RequestFactory()
        request=self.factory.get("/taskList")
        request.user=AnonymousUser()
        response=event(request)
        self.assertEquals(response.status_code,302)

# Anomynous person trying to access calendar
class AnomCalTest(TestCase):       
    def test_calendarEvent1(self):
        self.factory = RequestFactory()
        request=self.factory.get("/calendar")
        request.user=AnonymousUser()
        response=event(request)
        self.assertEquals(response.status_code,302)

# Known person trying to access calendar
class KnownCalTest(TestCase):       
    def test_calEvent2(self):
        self.factory = RequestFactory()
        request=self.factory.get("/calendar")
        request.user = User.objects.create_user(username='Owen', email='olr7ms@virginia.edu', password='WOW')
        response=event(request)
        self.assertEquals(response.status_code,200)

# Known person trying to access taskList
class KnownTaskListTest(TestCase):       
    def test_tasklistEvent2(self):
        self.factory = RequestFactory()
        request=self.factory.get("/taskList")
        request.user = User.objects.create_user(username='Owen', email='olr7ms@virginia.edu', password='WOW')
        response=event(request)
        self.assertEquals(response.status_code,200)

# Known person trying to access calendar/event/new
class KnownCalEventNewTest(TestCase):       
    def test_calendarevetnEvent2(self):
        self.factory = RequestFactory()
        request=self.factory.get("/calendar/event/new/")
        request.user = User.objects.create_user(username='Owen', email='olr7ms@virginia.edu', password='WOW')
        response=event(request)
        self.assertEquals(response.status_code,200)

# Known person trying to access event
class KnownEventTest(TestCase):       
    def test_eventEvent2(self):
        self.factory = RequestFactory()
        request=self.factory.get("/event")
        request.user = User.objects.create_user(username='Owen', email='olr7ms@virginia.edu', password='WOW')
        response=event(request)
        self.assertEquals(response.status_code,200)

# Known person trying to access edit
class KnownEditTest(TestCase):       
    def test_editEvent2(self):
        self.factory = RequestFactory()
        request=self.factory.get("/edit")
        request.user = User.objects.create_user(username='Owen', email='olr7ms@virginia.edu', password='WOW')
        response=event(request)
        self.assertEquals(response.status_code,200)

# Testing the Event model
class EventTest(TestCase):
    # Making two users and makig event objects
    def setUp(self):
        User = get_user_model()
        user1 = User.objects.create_user(username='Owen', email='olr7ms@virginia.edu', password='WOW')
        user1.save()
        user2 = User.objects.create_user(username='Luke', email='olr7ms@gmail.edu', password='Tester')
        user2.save()
        timestamp = date.today()

        Event.objects.create( title='CS3240 TestCase', description='We are testing here', start_time=date.today(), end_time=date.today(), author=user1, start_time_string='10:15', end_time_string='11:50')
        Event.objects.create( title='Hello', description='description', start_time=date.today(), end_time=date.today(), author=user2, start_time_string='10:15', end_time_string='11:50')

    # Testin the event
    def test_event(self):
        User = get_user_model()
        user = User.objects.get(username='Owen')
        event = Event.objects.get(title="CS3240 TestCase")
        entry_string = user.username + " " + event.title + " Event " + "11/30/2021"
        self.assertEquals(entry_string, "Owen CS3240 TestCase Event " + "11/30/2021")

    # Checking to see that the two events are made
    def two_events(self):
        self.assertEquals(Event.objects.all().count(), 2)

    # Correctly returns the infomation of two users and events
    def test_two_events(self):
        User = get_user_model()
        user1 = User.objects.get(username='Owen')
        user2 = User.objects.get(username='Luke')
        event1 = Event.objects.get(title="CS3240 TestCase")
        event2 = Event.objects.get(title="Hello")

        firstEvent = user1.username + " " + event1.title + " Event " + "11/30/2021"
        self.assertEquals(firstEvent, "Owen CS3240 TestCase Event " + "11/30/2021")

        secondEvent = user2.username + " " + event2.title + " Event " + "11/30/2021"
        self.assertEquals(secondEvent, "Luke Hello Event " + "11/30/2021")


# More Event test
class MoreEventTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='Owen', email='olr7ms@virginia.edu', password='WOW')
        self.user.save()
        self.timestamp = date.today()
        self.theEvent = Event( title='Hello', description='description', start_time=date.today(), end_time= date.today(), author=self.user, start_time_string='10:15', end_time_string='11:50')
        self.theEvent.save()

    def test_description(self):
        self.assertEqual(self.theEvent.description, 'description')

    def test_update_description(self):
        self.theEvent.description = 'new description'
        self.theEvent.save()
        self.assertEqual(self.theEvent.description, 'new description')

    def test_update_title(self):
        self.theEvent.title = 'new title'
        self.theEvent.save()
        self.assertEqual(self.theEvent.title, 'new title')

    def test_update_end_time(self):
        self.theEvent.end_time = self.timestamp + timedelta(days=2)
        self.theEvent.save()
        self.assertEqual(self.theEvent.end_time, self.timestamp + timedelta(days=2))
    
    def test_update_start_time(self):
        self.theEvent.start_time = self.timestamp + timedelta(days=1)
        self.theEvent.save()
        self.assertEqual(self.theEvent.start_time, self.timestamp + timedelta(days=1))


# Checking the delete user
class DeleteTest(TestCase):
    # Create a user with username Owen
    def setUp(self):
        User = get_user_model()
        user = User.objects.create(username='Owen')
        user.set_password('TestingPassword')
        user.save()

    # Tests to make sure that it correctly deletes user
    def test_delete_user(self):
        c = Client()
        User = get_user_model()
        user = User.objects.get(username='Owen')
        logged_in = c.login(username='Owen', password='TestingPassword')
        self.assertTrue(logged_in)
        user.delete()
        logged_in = c.login(username='Owen', password='TestingPassword')
        self.assertFalse(logged_in)


# Test the functionality of views
class VeiwsTest(TestCase):
    # Make users and events
    def setUp(self):
        User = get_user_model()
        user1 = User.objects.create(username='Ed')
        user1.set_password('passworda')
        user1.save()
        user2 = User.objects.create(username='Mike')
        user2.set_password('passwordb')
        user2.save()
        user3 = User.objects.create(username='Sav')
        user3.set_password('passwordc')
        user3.save()
        user4 = User.objects.create(username='Madison')
        user4.set_password('passwordd')
        user4.save()
        # Make two events
        Event.objects.create( title='CS3240 TestCase', description='We are testing here', start_time=date.today(), end_time=date.today(), author=user1, start_time_string='10:15', end_time_string='11:50')
        Event.objects.create( title='Hello', description='description', start_time=date.today(), end_time=date.today(), author=user3, start_time_string='10:15', end_time_string='11:50')

    # Test Calendar Response with a login user
    def test_calendar(self):
        c = Client()
        c.login( username = 'Ed', password = 'passworda' )
        response = c.get( reverse( 'oauth_app:calendar'), secure=True )
        self.assertEquals( response.status_code, 200 )


    # Test to check previous month
    def test_prev_month(self):
        User = get_user_model()
        user = User.objects.get(username='Ed')
        TheEvent = Event.objects.get(title="CS3240 TestCase")

        c = Client()
        c.login( username = 'Ed', password = 'passworda' )
        response = c.get( reverse( 'oauth_app:calendar'), secure=True )
        entry_list = response.context['prev_month']
        self.assertEquals( entry_list, 'month=2021-11' )

    # Test to check previous month
    def test_prev_month1(self):
        User = get_user_model()
        user = User.objects.get(username='Sav')
        TheEvent = Event.objects.get(title='Hello')

        c = Client()
        c.login( username = 'Sav', password = 'passwordc' )
        response = c.get( reverse( 'oauth_app:calendar'), secure=True )
        entry_list = response.context['prev_month']
        self.assertEquals( entry_list, 'month=2021-11')

    # Test to check next month
    def test_next_month(self):
        User = get_user_model()
        user = User.objects.get(username='Ed')
        TheEvent = Event.objects.get(title="CS3240 TestCase")

        c = Client()
        c.login( username = 'Ed', password = 'passworda' )
        response = c.get( reverse( 'oauth_app:calendar'), secure=True )
        entry_list = response.context['next_month']
        self.assertEquals( entry_list, 'month=2022-1' )

    # Test to check next month
    def test_next_month1(self):
        User = get_user_model()
        user = User.objects.get(username='Sav')
        TheEvent = Event.objects.get(title='Hello')
        c = Client()
        c.login( username = 'Sav', password = 'passwordc' )
        response = c.get( reverse('oauth_app:calendar'), secure=True )
        entry_list = response.context['next_month']
        self.assertEquals( entry_list, 'month=2022-1')

    # Test to make sure that the next month is correct
    def test_date(self):
        User = get_user_model()
        user = User.objects.get(username='Ed')
        date1 = pytz.utc.localize(datetime.datetime.now())
        date2 = date1 - timedelta( days = 6 )
        date3 = date1 - timedelta( days = 20 )
        Event.objects.create( title='CS3240 TestCase', description='We are testing here', start_time=date1,
         end_time=date1, author=user, start_time_string='10:15', end_time_string='11:50')
        Event.objects.create( title='Beta TestCase', description='We are testing here', start_time=date2,
         end_time=date2, author=user, start_time_string='10:15', end_time_string='11:50')
        Event.objects.create( title='Beta2', description='We are testing here', start_time=date3,
         end_time=date3, author=user, start_time_string='10:15', end_time_string='11:50')

        c = Client()
        c.login( username = 'Ed', password = 'passworda')
        response = c.get( reverse( 'oauth_app:calendar'), secure=True )
        entry_list = response.context['next_month']
        self.assertEquals( entry_list, 'month=2022-1')


        
# RESOURCES USED FOR TESTING
# - Help from TA on small problems
# - referenced https://docs.djangoproject.com/en/3.2/topics/testing/tools/
# - referenced https://docs.djangoproject.com/en/3.2/topics/testing/advanced/
# - referenced https://stackoverflow.com/questions/7304248/how-should-i-write-tests-for-forms-in-django
# - Also watched this video but proved to be pretty useless: https://www.youtube.com/watch?v=6tNS--WetLI