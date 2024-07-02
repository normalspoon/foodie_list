from django.db import models


from django.contrib.auth.models import User

# Create your models here.
  
class Restaurant(models.Model):
   place_id = models.CharField(primary_key=True, max_length=50)
   name = models.CharField(max_length=50)
   address = models.TextField()
   location = models.CharField(max_length=300)
   rating = models.DecimalField(decimal_places=1, max_digits=2)



class Review(models.Model):
  comments = models.CharField(max_length=50)
  img_url = models.CharField(max_length=200)
  stars = models.IntegerField()
   
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  Restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)