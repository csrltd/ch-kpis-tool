from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class UserRegistration(UserCreationForm):
    phone_number = forms.CharField(max_length=255)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name',
                  'phone_number', 'email', 'password1', 'password2']
 
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            raise forms.ValidationError('Please enter your email address', code='invalid_email')
        return email
    
    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if not first_name:
            raise forms.ValidationError('Please enter your first name', code='invalid_first_name')
        return first_name  

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')  
        if not last_name:
            raise forms.ValidationError('Please enter your last name', code='invalid_last_name')
        return last_name

