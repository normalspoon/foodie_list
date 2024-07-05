from django import forms
from django.forms import ModelForm
from .models import Review, Photo

class ReviewForm(ModelForm):
    photo = forms.ImageField(required=False)

    class Meta:
        model = Review
        fields = ['comments', 'img_url', 'stars', 'photo']