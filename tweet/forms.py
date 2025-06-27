from django import forms
from .models import Tweet 

class TweetForm(forms.ModelForm):
    class Meta:
        model = Tweet
        fields = ['text', 'photo']

    class UserRegistrationForm(forms.Form):
        username = forms.CharField(max_length=150)
        email = forms.EmailField()
        password = forms.CharField(widget=forms.PasswordInput)