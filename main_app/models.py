from django.db import models

from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
  name = models.CharField(max_length=50, default='User')
  username = models.CharField(max_length=50)
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  
  def __str__(self):
   return f'{self.name} ({self.id})'
  
class Restaurant(models.Model):
   name = models.CharField(max_length=50)
   address = models.TextField()
   location = models.CharField(max_length=300)
   rating = models.DecimalField()


# class Review(models.Model):
  