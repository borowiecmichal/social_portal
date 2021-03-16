import datetime

from django.contrib.auth.forms import SetPasswordForm, UserCreationForm, UsernameField
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django import forms

from portal_app.models import Photo, Comment


# class RegistrationForm(forms.Form): #dodać walidatory albo UserRegistrationForm/SignUpYUser
#     username = forms.CharField(label='Nazwa użytkownika', max_length=64)
#     first_name = forms.CharField(label='Imię')
#     last_name = forms.CharField(label='Nazwisko')
#     password = forms.CharField(label='Hasło', widget=forms.PasswordInput, validators=[validate_password])
#     password2 = forms.CharField(label='Hasło', widget=forms.PasswordInput)
#     email = forms.EmailField(label='e-mail')
#     motorcycle = forms.CharField(max_length=64)
#     date_of_birth = forms.DateField(widget=forms.SelectDateWidget(years=range(1920, datetime.datetime.now().year + 1)),
#                                     initial=datetime.date(year=datetime.date.today().year - 10,
#                                                           month=datetime.date.today().month,
#                                                           day=datetime.date.today().day))
#     city = forms.CharField(max_length=64)

class RegistrationForm(UserCreationForm):  # dodać walidatory albo UserRegistrationForm/SignUpYUser
    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email")
        field_classes = {'username': UsernameField}

    motorcycle = forms.CharField(max_length=64, label='Motocykl')
    date_of_birth = forms.DateField(widget=forms.SelectDateWidget(years=range(1920, datetime.datetime.now().year + 1)),
                                    initial=datetime.date(year=datetime.date.today().year - 18,
                                                          month=datetime.date.today().month,
                                                          day=datetime.date.today().day), label='Data urodzenia')
    city = forms.CharField(max_length=64, label='Miasto')


class LoginForm(forms.Form):
    username = forms.CharField(label='Nazwa użytkownika', max_length=64)
    password = forms.CharField(label='Hasło', widget=forms.PasswordInput)


class ImageForm(ModelForm):
    class Meta:
        model = Photo
        exclude = ['user']


class EditUserForm(forms.Form):
    username = forms.CharField(label='Nazwa użytkownika', max_length=64)
    first_name = forms.CharField(label='Imię')
    last_name = forms.CharField(label='Nazwisko')
    email = forms.EmailField(label='e-mail')
    motorcycle = forms.CharField(max_length=64)
    date_of_birth = forms.DateField(widget=forms.SelectDateWidget(years=range(1920, datetime.datetime.now().year + 1)),
                                    initial=datetime.date(year=datetime.date.today().year - 10,
                                                          month=datetime.date.today().month,
                                                          day=datetime.date.today().day))
    city = forms.CharField(max_length=64)


class AddCommentToPostForm(ModelForm):
    class Meta:
        model = Comment
        exclude = ['photo', 'user', 'date_add']


class MessageForm(forms.Form):
    message = forms.CharField(label='')
