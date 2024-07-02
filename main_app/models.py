from django.db import models

from django.contrib.auth.models import User

# Create your models here.
  
class Restaurant(models.Model):
   name = models.CharField(max_length=50)
   address = models.TextField()
   location = models.CharField(max_length=300)
   rating = models.DecimalField(decimal_places=1, max_digits=2)
   place_id = models.CharField(max_length=100, unique=True)
  
   def __str__(self):
     return self.name
    

   


class Review(models.Model):
  comments = models.CharField(max_length=50)
  img_url = models.CharField(max_length=200)
  stars = models.IntegerField()
   
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  Restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
  
  def __str__(self):
    return f"Review by {self.user.username} for {self.restaurant.name}"
  
