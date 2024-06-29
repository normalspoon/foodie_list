from django.shortcuts import render

# Create your views here.
def home(request):
  return render(request, 'home.html')

def myLists(request):
  return render(request, 'myLists.html')

def myMap(request):
  return render(request, 'myMap.html')
