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
import calendar
from django.test import TestCase
import pytz
import datetime


from django.test import TestCase
from django.utils import timezone

from .views import *

# Create your tests here.

# Testing Models

# Testing the Class Model
class ClassModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        Class.objects.create(name='CS3240', upload='True')

    def test_name_label(self):
        course = Class.objects.get(id=1)
        field_label = course._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'name')

    def test_upload_label(self):
        course = Class.objects.get(id=1)
        field_label = course._meta.get_field('upload').verbose_name
        self.assertEqual(field_label, 'upload')

    def test_name_max_length(self):
        course = Class.objects.get(id=1)
        max_length = course._meta.get_field('name').max_length
        self.assertEqual(max_length, 255)

    def test_course_name(self):
        course = Class.objects.get(id=1)
        self.assertEqual(str(course), 'Class object (1)')

# Testing Classes and students models
class ClassesAndStudentsModelTest(TestCase):
    @classmethod
    def setUp(self):
        self.user = User.objects.create_user(username='Owen', email='olr7ms@virginia.edu', password='WOW')
        self.user.save()
        self.course = Class.objects.create(name='CS3240', upload='True')
        self.course.save()
        ClassesAndStudents.objects.create(student=self.user, Class=self.course)

    def test_student_label(self):
        course = ClassesAndStudents.objects.get(id=1)
        field_label = course._meta.get_field('student').verbose_name
        self.assertEqual(field_label, 'student')

    def test_class_label(self):
        course = ClassesAndStudents.objects.get(id=1)
        field_label = course._meta.get_field('Class').verbose_name
        self.assertEqual(field_label, 'Class')

    def test_course_update_course_name(self):
        self.course.name = 'How to dance'
        self.course.save()
        self.assertEqual(self.course.name, 'How to dance')

    def test_courseStudent_name(self):
        course = ClassesAndStudents.objects.get(id=1)
        self.assertEqual(str(course), 'ClassesAndStudents object (1)')

class viewAllClasses_test(TestCase):
    def setUp(self):
        User = get_user_model()
        user1 = User.objects.create(username='Owen')
        user1.set_password('password!')
        user1.save()

        Class.objects.create(name='CS3240', upload='True')
        Class.objects.create(name='CS4102', upload='True')
        Class.objects.create(name='CS31O2', upload='True')
        Class.objects.create(name='CS2150', upload='True')
        Class.objects.create(name='CS4800', upload='True')

    def test_numClasses(self):   
        self.assertEquals(Class.objects.all().count(), 5)

    def test_delete_Class(self):
        TheClass = Class.objects.get(name="CS3240")
        self.assertEquals(Class.objects.all().count(), 5)
        TheClass.delete()
        self.assertEquals(Class.objects.all().count(), 4)

    def test_response(self):
        User = get_user_model()
        user = User.objects.get(username='Owen')
        TheClass = Class.objects.get(name="CS3240")

        c = Client()
        c.login( username = 'Owen', password = 'password!' )
        response = c.get( reverse('classes'), secure=True )
        #class_list = response.context['viewAllClasses']
        self.assertEquals( response.status_code, 200 )

    def test_view(self):
        User = get_user_model()
        user = User.objects.get(username='Owen')
        TheClass = Class.objects.get(name="CS3240")

        c = Client()
        c.login( username = 'Owen', password = 'password!' )
        response = c.get( reverse('classes'), secure=True )
        class_list = response.context['classes']
        self.assertEquals(class_list.all().count(), 0)

class test_veiws(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='Owen', email='olr7ms@virginia.edu', password='WOW')
        self.user.save()
        self.course = Class.objects.create(name='CS3240', upload='True')
        self.course.save()
        ClassesAndStudents.objects.create(student=self.user, Class=self.course)

    def test_addClass(self):
        c = Client()
        c.login( username = 'Owen', password = 'WOW' )
        response = c.get( reverse('classes'), secure=True )
        class_list = response.context['classes']
        self.assertEquals(class_list.all().count(), 1)

    def test_add_another_class(self):
        course1 = Class.objects.create(name='CS4102', upload='True')
        course1.save()
        ClassesAndStudents.objects.create(student=self.user, Class=course1)
        c = Client()
        c.login( username = 'Owen', password = 'WOW' )
        response = c.get( reverse('classes'), secure=True )
        class_list = response.context['classes']
        self.assertEquals(class_list.all().count(), 2)

    def test_add_another_class(self):
        course2 = Class.objects.create(name='CS4102', upload='True')
        course2.save()
        ClassesAndStudents.objects.create(student=self.user, Class=course2)
        course3 = Class.objects.create(name='CS3102', upload='True')
        course3.save()
        ClassesAndStudents.objects.create(student=self.user, Class=course3)
        course4 = Class.objects.create(name='CS4800', upload='True')
        course4.save()
        ClassesAndStudents.objects.create(student=self.user, Class=course4)
        course5 = Class.objects.create(name='CS3501', upload='True')
        course5.save()
        ClassesAndStudents.objects.create(student=self.user, Class=course5)
        c = Client()
        c.login( username = 'Owen', password = 'WOW' )
        response = c.get( reverse('classes'), secure=True )
        class_list = response.context['classes']
        self.assertEquals(class_list.all().count(), 5)

class AnomGalleryTest(TestCase):       
    def test_classClassroom(self):
        self.factory = RequestFactory()
        request=self.factory.get("/class/classroom")
        request.user=AnonymousUser()
        response=viewAllClasses(request)
        self.assertEquals(response.status_code,302)

class AnomAddTest(TestCase):       
    def test_classaddClass(self):
        self.factory = RequestFactory()
        request=self.factory.get("/class/addClass")
        request.user=AnonymousUser()
        response=addClass(request)
        self.assertEquals(response.status_code,302)

class AnomViewTest(TestCase):       
    def test_viewClass(self):
        self.factory = RequestFactory()
        request=self.factory.get("/class/viewClass")
        request.user=AnonymousUser()
        response=addClass(request)
        self.assertEquals(response.status_code,302)

class KnownViewTest(TestCase):       
    def test_viewClass1(self):
        self.factory = RequestFactory()
        request=self.factory.get("/class/viewClass")
        request.user = User.objects.create_user(username='Owen', email='olr7ms@virginia.edu', password='WOW')
        response=addClass(request)
        self.assertEquals(response.status_code,200)

class KnownAddTest(TestCase):       
    def test_addClass1(self):
        self.factory = RequestFactory()
        request=self.factory.get("/class/addClass")
        request.user = User.objects.create_user(username='Owen', email='olr7ms@virginia.edu', password='WOW')
        response=addClass(request)
        self.assertEquals(response.status_code,200)

class KnownGalleryTest(TestCase):       
    def test_classroom1(self):
        self.factory = RequestFactory()
        request=self.factory.get("/class/classroom")
        request.user = User.objects.create_user(username='Owen', email='olr7ms@virginia.edu', password='WOW')
        response=viewAllClasses(request)
        self.assertEquals(response.status_code,200)


        
# RESOURCES USED FOR TESTING
# - Help from TA on small problems
# - referenced https://docs.djangoproject.com/en/3.2/topics/testing/tools/
# - referenced https://docs.djangoproject.com/en/3.2/topics/testing/advanced/
# - referenced https://stackoverflow.com/questions/7304248/how-should-i-write-tests-for-forms-in-django
# - Also watched this video but proved to be pretty useless: https://www.youtube.com/watch?v=6tNS--WetLI