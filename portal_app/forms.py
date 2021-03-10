from django.forms import ModelForm
from django import forms

from portal_app.models import Photo


class RegistrationForm(forms.Form):
    username = forms.CharField(label='Nazwa użytkownika', max_length=64)
    first_name = forms.CharField(label='Imię')
    last_name = forms.CharField(label='Nazwisko')
    password = forms.CharField(label='Hasło', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Hasło', widget=forms.PasswordInput)
    email = forms.EmailField(label='e-mail')

class LoginForm(forms.Form):
    username = forms.CharField(label='Nazwa użytkownika', max_length=64)
    password = forms.CharField(label='Hasło', widget=forms.PasswordInput)


class ImageForm(ModelForm):
    class Meta:
        model = Photo
        exclude = ['user']
