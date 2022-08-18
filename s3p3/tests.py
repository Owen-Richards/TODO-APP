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
from classes.models import ClassesAndStudents, Class
from django.shortcuts import render, redirect
from .models import Folder, PDF
from django.contrib.auth.decorators import login_required
from classes.models import ClassesAndStudents, Class

from .models import *
import calendar
from django.test import TestCase
import pytz
import datetime


from django.test import TestCase
from django.utils import timezone

from .views import *

# Create your tests here.

class FolderModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        Folder.objects.create(name='CS3240 Homework')
        Folder.objects.create(name='CS4102 Homework')

    def test_name_label(self):
        course = Folder.objects.get(id=1)
        field_label = course._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'name')

    def test_name_max_length(self):
        course = Folder.objects.get(id=1)
        max_length = course._meta.get_field('name').max_length
        self.assertEqual(max_length, 100)

    def test_course_name(self):
        course = Folder.objects.get(id=1)
        self.assertEqual(str(course), 'CS3240 Homework')
    
    def test_course_name_id2(self):
        course = Folder.objects.get(id=2)
        self.assertEqual(str(course), 'CS4102 Homework')

class PDFTest(TestCase):
    @classmethod
    def setUp(self):
        self.user = User.objects.create_user(username='Owen', email='olr7ms@virginia.edu', password='WOW')
        self.user.save()
        self.course = Class.objects.create(name='CS3240', upload='True')
        self.course.save()
        self.factory = RequestFactory()
        request=self.factory.get("/class/viewClass")
        request.user = self.user
        data=request.POST
        file=request.FILES.get('pdf')
        pdf = PDF.objects.create(category=self.course,description='This is the first PDF of many',PDF=file,student=self.user)
        PDF.objects.create(category=self.course,description='hello',PDF=file,student=self.user)
        PDF.objects.create(category=self.course,description='Another One',PDF=file,student=self.user)

    def test_student(self):
        thePDF = PDF.objects.get(id=1)
        field_label = thePDF._meta.get_field('student').verbose_name
        self.assertEqual(field_label, 'student')

    def test_cateory(self):
        thePDF = PDF.objects.get(id=1)
        field_label = thePDF._meta.get_field('category').verbose_name
        self.assertEqual(field_label, 'category')

    def test_PDF(self):
        thePDF = PDF.objects.get(id=1)
        field_label = thePDF._meta.get_field('PDF').verbose_name
        self.assertEqual(field_label, 'PDF')

    def test_description(self):
        thePDF = PDF.objects.get(id=1)
        field_label = thePDF._meta.get_field('description').verbose_name
        self.assertEqual(field_label, 'description')

    def test_checkingPDF(self):
        thePDF = PDF.objects.get(id=1)
        self.assertEqual(str(thePDF), 'This is the first PDF of many')

    def test_checkingAddPDF(self):
        self.assertEquals(PDF.objects.all().count(), 3)    
    
    def test_deletePDF(self):
        ThePDF = PDF.objects.get(description="hello")
        ThePDF.delete()
        self.assertEquals(PDF.objects.all().count(), 2)   

class AnomGalleryTest(TestCase):       
    def test_gallery(self):
        self.factory = RequestFactory()
        request=self.factory.get("/gallery")
        request.user=AnonymousUser()
        response=gallery(request)
        self.assertEquals(response.status_code,302)

class AnomAddTest(TestCase):       
    def test_add(self):
        self.factory = RequestFactory()
        request=self.factory.get("/add")
        request.user=AnonymousUser()
        response=addpdf(request)
        self.assertEquals(response.status_code,302)

class KnownAddTest(TestCase):       
    def test_add1(self):
        self.factory = RequestFactory()
        request=self.factory.get("/add")
        request.user = User.objects.create_user(username='Owen', email='olr7ms@virginia.edu', password='WOW')
        response=addpdf(request)
        self.assertEquals(response.status_code,200)

class KnownGalleryTest(TestCase):       
    def test_gallery1(self):
        self.factory = RequestFactory()
        request=self.factory.get("/gallery")
        request.user = User.objects.create_user(username='Owen', email='olr7ms@virginia.edu', password='WOW')
        response=gallery(request)
        self.assertEquals(response.status_code,200)



# RESOURCES USED FOR TESTING
# - Help from TA on small problems
# - referenced https://docs.djangoproject.com/en/3.2/topics/testing/tools/
# - referenced https://docs.djangoproject.com/en/3.2/topics/testing/advanced/
# - referenced https://stackoverflow.com/questions/7304248/how-should-i-write-tests-for-forms-in-django
# - Also watched this video but proved to be pretty useless: https://www.youtube.com/watch?v=6tNS--WetLI

