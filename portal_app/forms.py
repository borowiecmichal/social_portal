# from django.forms import forms, ModelForm
from django import forms


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