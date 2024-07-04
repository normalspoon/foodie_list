from django.db import models

from django.contrib.auth.models import User

# Create your models here.
  
class Restaurant(models.Model):
   place_id = models.CharField(primary_key=True, max_length=50)
   name = models.CharField(max_length=50)
   address = models.TextField(max_length = 200)
   location = models.CharField(max_length=300)
   photo_url = models.CharField(max_length=200, default='')
  
   def __str__(self):
     return self.name
    

   


class Review(models.Model):
  RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]
  
  comments = models.TextField()
  img_url = models.CharField(max_length=200)
  stars = models.IntegerField(choices=RATING_CHOICES)
   
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
  
  def __str__(self):
    return f"Review by {self.user.username} for {self.restaurant.name}"
  
class Photo(models.Model):
  url = models.CharField(max_length=200)
  restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
  
  def __str__(self):
    return f"Photo for restaurant_id: {self.restaurant_id} @{self.url}"