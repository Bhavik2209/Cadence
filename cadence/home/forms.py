from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User

class UserRegForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'bg-gray-50 border-none text-gray-900 sm:text-sm rounded-lg focus:ring-primary-600 focus:border-none block w-full p-2.5 dark:bg-gray-700 dark:border-none dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-none',
        'placeholder': 'name@company.com',
        'style': 'outline: none;'  # Additional inline style for outline
    }),
    )
    
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'bg-gray-50 border-none text-gray-900 sm:text-sm rounded-lg focus:ring-primary-600 focus:border-none block w-full p-2.5 dark:bg-gray-700 dark:border-none dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-none',
        'placeholder': 'Username',
        'style': 'outline: none;'  # Additional inline style for outline
    }))
    
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'bg-gray-50 border-none text-gray-900 sm:text-sm rounded-lg focus:ring-primary-600 focus:border-none block w-full p-2.5 dark:bg-gray-700 dark:border-none dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-none',
        'placeholder': 'Password',
        'style': 'outline: none;'  # Additional inline style for outline
    }))
    
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'bg-gray-50 border-none text-gray-900 sm:text-sm rounded-lg focus:ring-primary-600 focus:border-none block w-full p-2.5 dark:bg-gray-700 dark:border-none dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-none',
        'placeholder': 'Confirm Password',
        'style': 'outline: none;'  # Additional inline style for outline
    }))
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        
class UserLoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
