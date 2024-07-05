import uuid
import boto3
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from .models import Review, Restaurant, Photo
from .forms import ReviewForm
from django.urls import reverse_lazy
from decouple import config
from .models import Restaurant
import requests
import os
from django.http import HttpResponse


# Create your views here.
def home(request):
  restaurants = Restaurant.objects.all()
  context = {
    'restaurants': restaurants
    }
  
  return render(request, 'home.html', context)

def signup(request):
  error_message = ''
  if request.method == 'POST':
    print(request.POST)
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save()
      login(request, user)
      return redirect('home')
    else:
      error_message = 'Unable to sign up - try again.'
      print(form.errors)
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)

def places_details(request, place_id):
  api_key = config('GOOGLE_API_KEY')
  place_details_url = f'https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&key={api_key}'
  response = requests.get(place_details_url)
  place_details = response.json().get('result', {})

  name= place_details.get('name')
  address= place_details.get('formatted_address')
  location= place_details.get('geometry').get('location')
  opening_hours= place_details.get('current_opening_hours')
  photos= place_details.get('photos', [])

  
  photo_reference = None
  photo_url = None
  
  if photos:
  # the first photo in the photos
    photo_reference = photos[0].get('photo_reference')
    photo_url = f'https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference={photo_reference}&key={api_key}'
  
  
  
  restaurant, created = Restaurant.objects.get_or_create(
    place_id=place_id,
    defaults={
      'name': name, 
      'address': address, 
      'location': location, 
      'opening_hours': opening_hours,
      'photo_reference': photo_reference,
      'photo_url': photo_url,

    }
  )  
  
  # retrive reviews ordered by creatd_at in descending order
  # reviews = restaurant.review_set.all().order_by('-created_at')
  
  # add review form
  review_form = ReviewForm()

  return render(request, 'restaurants/detail.html', {
    'place_details': place_details, 'review_form': review_form, 'api_key': api_key, 'restaurant': restaurant
    })

@login_required
def myLists(request):
  return render(request, 'myLists.html')

@login_required
def myMap(request):
  return render(request, 'myMap.html')


class ReviewList(ListView):
  model = Review

class ReviewCreate(LoginRequiredMixin, CreateView):
    model = Review
    form_class = ReviewForm
    template_name = 'restaurants/review_form.html'

    def form_valid(self, form):
        place_id = self.kwargs['place_id']
        restaurant = get_object_or_404(Restaurant, place_id=place_id)
        form.instance.restaurant = restaurant
        form.instance.user = self.request.user
        response = super().form_valid(form)

        photo_file = self.request.FILES.get('photo', None)
        if photo_file:
            s3 = boto3.client('s3')
            key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
            try:
                bucket = os.environ['S3_BUCKET']
                s3.upload_fileobj(photo_file, bucket, key)
                url = f"{os.environ['S3_BASE_URL']}{key}"
                Photo.objects.create(url=url, review_id=self.object.id)
                print(f"Photo uploaded to {url}")
            except Exception as e:
                print('An error occurred uploading file to S3')
                print(e)

        return response

    def get_success_url(self):
        return reverse_lazy('places_details', kwargs={'place_id': self.kwargs['place_id']})


class ReviewUpdate(LoginRequiredMixin, UpdateView):
    model = Review
    form_class = ReviewForm
    template_name = 'restaurants/review_form.html'

    def form_valid(self, form):
        response = super().form_valid(form)

        photo_file = self.request.FILES.get('photo')
        if photo_file:
            s3 = boto3.client('s3')
            key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
            try:
                bucket = os.environ['S3_BUCKET']
                print(f"Uploading {photo_file.name} to bucket {bucket} with key {key}")
                s3.upload_fileobj(photo_file, bucket, key)
                url = f"{os.environ['S3_BASE_URL']}{bucket}/{key}"
                print(f"Uploaded to {url}")
                Photo.objects.create(url=url, review_id=self.object.id)
                print(f"Photo object created with URL: {url}")
            except Exception as e:
                print('An error occurred uploading file to S3')
                print(e)

        return response

    def get_success_url(self):
        return reverse_lazy('places_details', kwargs={'place_id': self.object.restaurant.place_id})

  
class ReviewUpdate(LoginRequiredMixin, UpdateView):
  model = Review
  fields = ['comments', 'img_url', 'stars']
  
class ReviewDelete(LoginRequiredMixin, DeleteView):
  model = Review
  success_url = '/home'
  
@login_required
def test_upload(request):
    if request.method == 'POST':
        photo_file = request.FILES.get('photo', None)
        if photo_file:
            s3 = boto3.client('s3')
            key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
            try:
                bucket = os.environ['S3_BUCKET']
                base_url = os.environ['S3_BASE_URL']
                print(f"Uploading {photo_file.name} to bucket {bucket} with key {key}")
                s3.upload_fileobj(photo_file, bucket, key)
                url = f"{base_url}/{key}"
                print(f"Uploaded to {url}")
                return HttpResponse(f"File uploaded to {url}")
            except Exception as e:
                print('An error occurred uploading file to S3')
                print(e)
                return HttpResponse(f"Error: {e}", status=500)
    return render(request, 'test_upload.html')