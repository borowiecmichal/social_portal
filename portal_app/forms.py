import datetime

from django.contrib.auth.forms import SetPasswordForm
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django import forms

from portal_app.models import Photo, Comment


class RegistrationForm(forms.Form):
    username = forms.CharField(label='Nazwa użytkownika', max_length=64)
    first_name = forms.CharField(label='Imię')
    last_name = forms.CharField(label='Nazwisko')
    password = forms.CharField(label='Hasło', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Hasło', widget=forms.PasswordInput)
    email = forms.EmailField(label='e-mail')
    motorcycle = forms.CharField(max_length=64)
    date_of_birth = forms.DateField(widget=forms.SelectDateWidget(years=range(1920, datetime.datetime.now().year + 1)),
                                    initial=datetime.date(year=datetime.date.today().year - 10,
                                                          month=datetime.date.today().month,
                                                          day=datetime.date.today().day))
    city = forms.CharField(max_length=64)


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