from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns=[
    path('classes', views.viewAllClasses, name='classes'),
    path('class/<str:pk>/', views.viewClass, name='viewClass'),
    path('addclass/', views.addClass, name='addclass'),
    path('deleteClass/<str:pk>', views.deleteClass, name='deleteClass'),
    path('addMessage/class/<str:pk>/',views.postMessage, name='messagePost'),
    path('message/<str:pk>', views.viewMessage, name='viewMessage'),
]