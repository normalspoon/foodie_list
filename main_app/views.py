from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from decouple import config
from .models import Restaurant
import requests

# Create your views here.
def home(request):
  return render(request, 'home.html')

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
  rating= place_details.get('rating')

  restaurant, created = Restaurant.objects.get_or_create(
    place_id=place_id,
    defaults={
      'name': name, 
      'address': address, 
      'location': location, 
      'rating': rating
    }
  )
  context = {
    'place_details': place_details,
    'api_key': api_key,
    'restaurant': restaurant,
  }

   
  return render(request, 'restaurants/detail.html', context)


def myLists(request):
  return render(request, 'myLists.html')

def myMap(request):
  return render(request, 'myMap.html')
