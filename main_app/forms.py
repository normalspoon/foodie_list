from django import forms
from django.forms import ModelForm
from .models import Review

class ReviewForm(ModelForm):
    photo = forms.ImageField(required=False)

    class Meta:
        model = Review
        fields = ['comments', 'stars', 'photo']