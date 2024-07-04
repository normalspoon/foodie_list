from django.contrib import admin

from .models import Review, Restaurant, Photo
# Register your models here.

admin.site.register(Review)
admin.site.register(Restaurant)
admin.site.register(Photo)


