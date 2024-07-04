from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from .models import Review, Restaurant
from .forms import ReviewForm
from django.urls import reverse_lazy
from decouple import config
from .models import Restaurant
import requests

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
  print(photos)
   # I dont think we need google places rating?
  # rating= place_details.get('rating') 
  
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
      # 'rating': rating
    }
  )  
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
    fields = ['comments', 'img_url', 'stars']
    template_name = 'restaurants/review_form.html'

    def form_valid(self, form):
        place_id = self.kwargs['place_id']
        restaurant = get_object_or_404(Restaurant, place_id=place_id)  
        form.instance.restaurant = restaurant
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('places_details', kwargs={'place_id': self.kwargs['place_id']})
  
class ReviewUpdate(LoginRequiredMixin, UpdateView):
  model = Review
  fields = ['comments', 'img_url', 'stars']
  
class ReviewDelete(LoginRequiredMixin, DeleteView):
  model = Review
  success_url = '/home'