from django.db import models

from django.contrib.auth.models import User

# Create your models here.
  
class Restaurant(models.Model):
   place_id = models.CharField(primary_key=True, max_length=50)
   name = models.CharField(max_length=50)
   address = models.TextField(max_length = 200)
   opening_hours = models.TextField(max_length = 1000, null=True, blank=True)
   location = models.CharField(max_length=100)
   photo_url = models.CharField(max_length=1000, default='')
   photo_reference = models.CharField(max_length=1000, default='')
  
   def __str__(self):
     return self.name
    

   


class Review(models.Model):
  RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]
  
  comments = models.TextField()
  stars = models.IntegerField(choices=RATING_CHOICES)
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
  created_at = models.DateTimeField(auto_now_add=True)
  
  def __str__(self):
    return f"Review by {self.user.username} for {self.restaurant.name}"

  
class Photo(models.Model):
  url = models.FileField(max_length=200)
  review = models.ForeignKey(Review, on_delete=models.CASCADE)
  
  def __str__(self):
    return f"Photo for review_id: {self.review_id} @{self.url}"

