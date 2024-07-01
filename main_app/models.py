from django.db import models

from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  
  
class Restaurant(models.Model):
   name = models.CharField(max_length=50)
   address = models.TextField()
   location = models.CharField(max_length=300)
   rating = models.DecimalField()


# class Review(models.Model):
  