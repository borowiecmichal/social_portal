from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import View
from django.views.generic import FormView, CreateView

from portal_app.forms import RegistrationForm, LoginForm, ImageForm, EditUserForm
from portal_app.models import Photo, Post, AdditionalInfo, Comment
from django.contrib.auth import views as auth_views


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
                    u = User.objects.create_user(username=form.cleaned_data['username'],
                                                 password=form.cleaned_data['password'],
                                                 first_name=form.cleaned_data['first_name'],
                                                 last_name=form.cleaned_data['last_name'],
                                                 email=form.cleaned_data['email'])
                    AdditionalInfo.objects.create(
                        user=u,
                        motorcycle=form.cleaned_data['motorcycle'],
                        date_of_birth=form.cleaned_data['date_of_birth'],
                        city=form.cleaned_data['city']
                    )

                except IntegrityError:
                    return render(request, 'registration.html', {'form': form, 'error': 'Użytkownik już istnieje'})
                except ValidationError as e:
                    return render(request, 'registration.html',
                                  {'form': form, 'error': f'Hasło nie spełnia wymagań: {e}'})

                return redirect(reverse('home'))


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
                return redirect(reverse('home'))
            else:
                return render(request, 'login.html', {'form': form, 'error': 'Błędne dane logowania'})
        else:
            return HttpResponse('BŁĄD')


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect(reverse('home'))


class UserProfileView(LoginRequiredMixin, View):
    def get(self, request, username):
        user = User.objects.get(username=username)
        content_post = Post.objects.filter(user=user).order_by('-date_add')
        content_photo = Photo.objects.filter(user=user).order_by('-date_add')
        context = {
            'user_requested': user,
            'content_post': content_post,
            'content_photo': content_photo,
        }
        return render(request, 'userprofileview.html', context)


# class PhotoCreateView(LoginRequiredMixin, CreateView):
#     model = Photo
#     fields = ['photo', 'description']
#     template_name = 'photo_create_form.html'
#
#     def form_valid(self, form):
#         user = self.request.user
#         form.instance.user = user
#         return super(PhotoCreateView,self).form_valid(form)
#
#     def get_success_url(self):
#         return reverse('user-profile', self.request.user.username)

class PhotoCreateView(LoginRequiredMixin, View):
    def get(self, request):
        form = ImageForm()
        return render(request, 'photo_create_form.html', {'form': form})

    def post(self, request):
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            newPhoto = Photo.objects.create(photo=request.FILES['photo'], user=request.user,
                                            description=form.cleaned_data['description'])
            return redirect(reverse('user-profile', kwargs={'username': request.user.username}))


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['content']
    template_name = 'post_create_form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('user-profile', kwargs={'username': self.request.user.username})


class ProfileEditView(View):
    def get(self, request, username):
        user = User.objects.get(username=username)
        form = EditUserForm(initial={
            'username': username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'motorcycle': user.additionalinfo.motorcycle,
            'date_of_birth': user.additionalinfo.date_of_birth,
            'city': user.additionalinfo.city
        })
        return render(request, 'editProfile.html', {'form': form})

    def post(self, request, username):
        form = EditUserForm(request.POST)
        user = User.objects.get(username=username)
        if form.is_valid():
            try:
                user = User.objects.get(username=username)
                user.username = form.cleaned_data['username']
                user.first_name = form.cleane_data['first_name']
                user.last_name = form.cleaned_data['last_name']
                user.email = form.cleaned_data['email']
                user.additionalinfo.motorcycle = form.cleaned_data['motorcycle']
                user.additionalinfo.date_of_birth = form.cleaned_data['date_of_birth']
                user.additionalinfo.city = form.cleaned_data['city']
                user.save()
            except IntegrityError:
                return render(request, 'editProfile.html', {'form': form, 'error': 'Podany login jest zajęty'})
        return redirect(reverse('user-profile', kwargs={'username': user.username}))


class CommentToPostAddView(LoginRequiredMixin, CreateView):
    model = Comment
    fields = ['content']
    template_name = 'portal_app/comment_form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('user-profile', kwargs={'username': self.request.user.username})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        commented_item = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        context["commented_item"] = commented_item
        return context
