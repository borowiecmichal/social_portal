from itertools import chain
from operator import attrgetter

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User, Group
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import View
from django.views.generic import FormView, CreateView, ListView, DetailView, DeleteView
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from portal_app.forms import RegistrationForm, LoginForm, ImageForm, EditUserForm, MessageForm
from portal_app.models import Photo, Post, AdditionalInfo, Comment, Category, Groupe, Messages, Like
from django.contrib.auth import views as auth_views

from portal_app.serializers import LikeSerializer, UserSerializer, GroupSerializer, PostSerializer, GroupeSerializer, \
    CategorySerializer, AdditionalInfoSerializer


class LandingView(View):
    def get(self, request):
        return render(request, 'landing_page.html')


# class UserRegistrationView(View):
#     def get(self, request):
#         form = RegistrationForm()
#         return render(request, 'registration.html', {'form': form})
#
#     def post(self, request):
#         form = RegistrationForm(request.POST)
#         if form.is_valid():
#             if form.cleaned_data['password'] == form.cleaned_data['password2']:
#                 try:
#                     # validate_password(password=form.cleaned_data['password'])
#                     u = User.objects.create_user(username=form.cleaned_data['username'],
#                                                  password=form.cleaned_data['password'],
#                                                  first_name=form.cleaned_data['first_name'],
#                                                  last_name=form.cleaned_data['last_name'],
#                                                  email=form.cleaned_data['email'])
#                     AdditionalInfo.objects.create(
#                         user=u,
#                         motorcycle=form.cleaned_data['motorcycle'],
#                         date_of_birth=form.cleaned_data['date_of_birth'],
#                         city=form.cleaned_data['city']
#                     )
#
#                 except IntegrityError:
#                     return render(request, 'registration.html', {'form': form, 'error': 'Użytkownik już istnieje'})
#                 except ValidationError as e:
#                     return render(request, 'registration.html',
#                                   {'form': form, 'error': f'Hasło nie spełnia wymagań: {e}'})
#
#                 return redirect(reverse('home'))

class UserRegistrationView(FormView):
    form_class = RegistrationForm
    template_name = 'registration.html'

    def get_success_url(self):
        return reverse('home')


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
                if request.GET.get('next'):
                    return redirect(request.GET.get('next'))
                return redirect(reverse('user-profile', kwargs={'username': user.username}))
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
        content_post = Post.objects.filter(user=user, group__isnull=True).order_by('-date_add')
        content_photo = Photo.objects.filter(user=user).order_by('-date_add')
        context = {
            'user_requested': user,
            'content_post': content_post,
            'content_photo': content_photo,
        }
        return render(request, 'userprofileview.html', context)


class LikePostView(View):
    def post(self, request, post_id):
        post = Post.objects.get(pk=post_id)
        post.likes += 1
        post.save()
        user = post.user
        return redirect(reverse('user-profile', kwargs={'username': user.username}))


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
                user.first_name = form.cleaned_data['first_name']
                user.last_name = form.cleaned_data['last_name']
                user.email = form.cleaned_data['email']
                user.additionalinfo.motorcycle = form.cleaned_data['motorcycle']
                user.additionalinfo.date_of_birth = form.cleaned_data['date_of_birth']
                user.additionalinfo.city = form.cleaned_data['city']
                user.additionalinfo.save()
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
        post = Post.objects.get(pk=self.kwargs.get('post_id'))
        return reverse('user-profile', kwargs={'username': post.user})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        commented_item = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        context["commented_item"] = commented_item
        return context


class CommentToPhotoAddView(LoginRequiredMixin, CreateView):
    model = Comment
    fields = ['content']
    template_name = 'portal_app/commentPhoto_form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.photo = get_object_or_404(Photo, pk=self.kwargs.get('photo_id'))
        return super().form_valid(form)

    def get_success_url(self):
        photo = Photo.objects.get(pk=self.kwargs.get('photo_id'))
        return reverse('user-profile', kwargs={'username': photo.user})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(self.kwargs.get('photo_id'))
        commented_item = get_object_or_404(Photo, pk=self.kwargs.get('photo_id'))

        context["commented_item"] = commented_item
        return context


###################GRUPY#########################

class GroupView(LoginRequiredMixin, ListView):
    model = Groupe
    paginate_by = 20


class GroupDetail(UserPassesTestMixin, LoginRequiredMixin, DetailView):
    def test_func(self):
        slug = self.kwargs.get("slug")
        groupe = Groupe.objects.get(slug=slug)
        user = self.request.user
        if groupe.users.filter(id=user.id).exists():
            return True
        else:
            return False

    model = Groupe


class GroupPostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['content']
    template_name = 'grouppost_create_form.html'

    def form_valid(self, form):
        group = Groupe.objects.get(slug=self.kwargs.get('slug'))
        form.instance.user = self.request.user
        form.instance.group = group
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('users-groups', kwargs={'username': self.request.user.username})


class GroupAppendView(LoginRequiredMixin, View):

    def get(self, request, slug):
        groupe = Groupe.objects.get(slug=slug)
        groupe.to_join.add(request.user)
        groupe.save()
        return redirect(reverse('groups'))


class GroupCreateView(LoginRequiredMixin, CreateView):
    model = Groupe
    fields = ['name', 'category']

    def form_valid(self, form):
        instance = form.save()
        instance.moderators.set([self.request.user])
        instance.users.set([self.request.user])
        instance.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('groups')


class UsersGroupeView(UserPassesTestMixin, LoginRequiredMixin, ListView):
    model = Groupe
    paginate_by = 20
    template_name = 'portal_app/usersgroups_list.html'

    def test_func(self):
        if self.request.user.username == self.kwargs.get("username"):
            return True
        else:
            return False

    def get_queryset(self):
        user = User.objects.get(username=self.kwargs.get('username'))
        return user.groupe_set.all() | user.groups_to_join.all()


class GroupeDelete(UserPassesTestMixin, LoginRequiredMixin, DeleteView):
    def test_func(self):
        slug = self.kwargs.get("slug")
        groupe = Groupe.objects.get(slug=slug)
        user = self.request.user
        if groupe.moderators.filter(id=user.id).exists():
            return True
        else:
            return False

    model = Groupe

    def get_success_url(self):
        return reverse('groups')


class GroupeRequests(UserPassesTestMixin, LoginRequiredMixin, View):
    def test_func(self):
        slug = self.kwargs.get("slug")
        groupe = Groupe.objects.get(slug=slug)
        user = self.request.user
        if groupe.moderators.filter(id=user.id).exists():
            return True
        else:
            return False

    def get(self, request, slug):
        group = Groupe.objects.get(slug=slug)
        requests_list = group.to_join.all()
        return render(request, 'requests_to_group.html', {
            'requests_list': requests_list,
            'group': group
        })


class GroupeRequestsAcceptUser(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        slug = self.kwargs.get("slug")
        groupe = Groupe.objects.get(slug=slug)
        user = self.request.user
        if groupe.moderators.filter(id=user.id).exists():
            return True
        else:
            return False

    def get(self, request, slug, username):
        group = Groupe.objects.get(slug=slug)
        usr = User.objects.get(username=username)
        group.to_join.remove(usr)
        group.users.add(usr)
        return redirect(reverse('group-requests', kwargs={'slug': group.slug}))


class GroupeRequestsRejectUser(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        slug = self.kwargs.get("slug")
        groupe = Groupe.objects.get(slug=slug)
        user = self.request.user
        if groupe.moderators.filter(id=user.id).exists():
            return True
        else:
            return False

    def get(self, request, slug, username):
        group = Groupe.objects.get(slug=slug)
        usr = User.objects.get(username=username)
        group.to_join.remove(usr)
        return redirect(reverse('group-requests', kwargs={'slug': group.slug}))


class GroupeLeave(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        slug = self.kwargs.get("slug")
        groupe = Groupe.objects.get(slug=slug)
        user = self.request.user
        if groupe.users.filter(id=user.id).exists():
            return True
        else:
            return False

    def get(self, request, slug):
        group = Groupe.objects.get(slug=slug)
        group.users.remove(request.user)
        if group.moderators.filter(id=request.user.id).exists():
            group.moderators.remove(request.user)
        return redirect(reverse('users-groups', kwargs={'username': request.user.username}))


########################### WIADOMOŚCI ############
class MessagesView(LoginRequiredMixin, ListView):
    model = User
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super(MessagesView, self).get_context_data(**kwargs)
        myUserObj = self.request.user
        for with_user in context['object_list']:
            unseen_to_me = Messages.objects.filter(from_user=with_user, to_user=myUserObj, seen=False)
            with_user.unseen = unseen_to_me.count()
        print(context['object_list'][2].unseen)
        return context

    template_name = 'portal_app/usersList_forMessages.html'


class MessagesWithUser(LoginRequiredMixin, View):
    def get(self, request, with_username):
        form = MessageForm()
        with_user = User.objects.get(username=with_username)
        messages_received = Messages.objects.filter(from_user=with_user, to_user=request.user)
        messages_send = Messages.objects.filter(to_user=with_user, from_user=request.user)
        for msg in messages_received.filter(seen=False):
            msg.seen = True
            msg.save()
        chained = sorted(list(chain(messages_received, messages_send)), key=attrgetter('date'))
        return render(request, 'conversation_template.html', {
            'messages': chained,
            'with_user': with_user,
            'form': form,
        })

    def post(self, request, with_username):
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.cleaned_data['message']
            from_user = request.user
            to_user = User.objects.get(username=with_username)
            Messages.objects.create(content=message, from_user=from_user, to_user=to_user)
            return redirect(reverse('messages-with-user', kwargs={'with_username': to_user.username}))


########################################################################################################################

#################################################  API  ################################################################

########################################################################################################################

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupeViewSet(viewsets.ModelViewSet):
    queryset = Groupe.objects.all()
    serializer_class = GroupeSerializer
    permission_classes = [permissions.IsAuthenticated]


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]


class AdditionalInfoSerializer(viewsets.ModelViewSet):
    queryset = AdditionalInfo.objects.all()
    serializer_class = AdditionalInfoSerializer
    permission_classes = [permissions.IsAuthenticated]



class LikeView(APIView):
    def get(self, request):
        likes = Like.objects.all()
        serializer = LikeSerializer(likes, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = LikeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
