from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from .models import Review, Restaurant
from django.urls import reverse_lazy
from decouple import config
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

  context = {
    'place_details': place_details,
    'api_key': api_key,
  }
  return render(request, 'restaurants/detail.html', context)


def myLists(request):
  return render(request, 'myLists.html')

def myMap(request):
  return render(request, 'myMap.html')


class ReviewList(ListView):
  model = Review

class ReviewCreate(CreateView):
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
  
class ReviewUpdate(UpdateView):
  model = Review
  fields = ['comments', 'img_url', 'stars']
  
class ReviewDelete(DeleteView):
  model = Review
  success_url = '/home'