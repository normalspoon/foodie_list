from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('details/<str:place_id>/', views.places_details, name='places_details'),
    path('myLists/', views.myLists, name='myLists'),
    path('myMap/', views.myMap, name='myMap'),
]