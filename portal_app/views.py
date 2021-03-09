from django.contrib.auth.models import User
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import FormView

from portal_app.forms import RegistrationForm


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
            print(form.cleaned_data['username'])
            if form.cleaned_data['password'] == form.cleaned_data['password2']:
                try:
                    User.objects.create_user(username=form.cleaned_data['username'],
                                             password=form.cleaned_data['password'],
                                             first_name=form.cleaned_data['first_name'],
                                             last_name=form.cleaned_data['last_name'],
                                             email=form.cleaned_data['email'])
                except IntegrityError:
                    return render(request, 'registration.html', {'form': form, 'error':'Użytkownik już istnieje'})
                return redirect('/')

class LoginView(View):
    def get(self, request):
        form = RegistrationForm()
        return render(request, 'registration.html', {'form': form})

    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data['username'])
            if form.cleaned_data['password'] == form.cleaned_data['password2']:
                try:
                    User.objects.create_user(username=form.cleaned_data['username'],
                                             password=form.cleaned_data['password'],
                                             first_name=form.cleaned_data['first_name'],
                                             last_name=form.cleaned_data['last_name'],
                                             email=form.cleaned_data['email'])
                except IntegrityError:
                    return render(request, 'registration.html', {'form': form, 'error':'Użytkownik już istnieje'})
                return redirect('/')