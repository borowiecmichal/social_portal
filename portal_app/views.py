from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import FormView

from portal_app.forms import RegistrationForm, LoginForm


class LandingView(View):
    def get(self, request):
        return render(request, 'landing_page.html')


class RegistrationView(View):
    def get(self, request):
        form = RegistrationForm()
        return render(request, 'registration.html', {'form': form})

    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['password'] == form.cleaned_data['password2']:
                try:
                    validate_password(password=form.cleaned_data['password'])
                    User.objects.create_user(username=form.cleaned_data['username'],
                                             password=form.cleaned_data['password'],
                                             first_name=form.cleaned_data['first_name'],
                                             last_name=form.cleaned_data['last_name'],
                                             email=form.cleaned_data['email'])
                except IntegrityError:
                    return render(request, 'registration.html', {'form': form, 'error': 'Użytkownik już istnieje'})
                except ValidationError as e:
                    return render(request, 'registration.html',
                                  {'form': form, 'error': f'Hasło nie spełnia wymagań: {e}'})

                return redirect(reverse('landing'))


class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(request, username=form.cleaned_data['username'],
                                password=form.cleaned_data['password'])
            if user:
                login(request, user)
                return redirect(reverse('landing'))
            else:
                return render(request, 'login.html', {'form': form, 'error': 'Błędne dane logowania'})
        else:
            return HttpResponse('BŁĄD')


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect(reverse('landing'))
