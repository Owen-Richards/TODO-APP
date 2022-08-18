from django.urls import path

from . import views

urlpatterns=[
    path('files/',views.gallery,name='gallery'),
    path('add/', views.addpdf,name='add'),
    path('pdf/<str:pk>/', views.viewpdf, name='pdf'),
    path('deletePDF/', views.deletePDF, name='deletePDF')

]