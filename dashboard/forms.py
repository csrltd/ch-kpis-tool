from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User



class UserRegistration(UserCreationForm):
    phone_number = forms.CharField(max_length=255)
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'phone_number', 'email', 'password1', 'password2']

