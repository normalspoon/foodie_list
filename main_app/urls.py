from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/signup/', views.signup, name='signup'),
    path('details/<str:place_id>/', views.places_details, name='places_details'),
    path('myLists/', views.myLists, name='myLists'),
    path('myMap/', views.myMap, name='myMap'),
    path('reviews/create/<str:place_id>/', views.ReviewCreate.as_view(), name='reviews_create'),
    path('reviews/<int:pk>/update/', views.ReviewUpdate.as_view(), name='reviews_update'),
    path('reviews/<int:pk>/delete/', views.ReviewDelete.as_view(), name='reviews_delete'),
    path('test-upload/', views.test_upload, name='test_upload'),
]
