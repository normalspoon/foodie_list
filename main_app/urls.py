from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('myLists/', views.myLists, name='myLists'),
    path('myMap/', views.myMap, name='myMap'),
]