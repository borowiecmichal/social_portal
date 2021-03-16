"""social_portal URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns, static
from django.urls import path
from portal_app.views import LandingView, RegistrationView, LoginView, LogoutView, UserProfileView, PhotoCreateView, \
    PostCreateView, ProfileEditView, CommentToPostAddView, GroupView, GroupDetail, GroupPostCreateView, GroupAppendView, \
    GroupCreateView, UsersGroupeView, CommentToPhotoAddView, MessagesView, MessagesWithUser, LikePostView
from social_portal import settings
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', LandingView.as_view(), name='home'),
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegistrationView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/<str:username>', UserProfileView.as_view(), name='user-profile'),
    path('add_photo/', PhotoCreateView.as_view(), name='add-photo'),
    path('add_post/', PostCreateView.as_view(), name='add-post'),
    path('like-post/<int:post_id>', LikePostView.as_view(), name='like-post'),
    path('profile/<str:username>/edit', ProfileEditView.as_view(), name='edit-user'),
    path(
        'change-password/',
        auth_views.PasswordChangeView.as_view(
            template_name='commons/change-password.html',
            success_url='/'
        ),
        name='change_password'
    ),
    path('comment-post/<int:post_id>', CommentToPostAddView.as_view(), name='comment-post'),
    path('comment-photo/<int:photo_id>', CommentToPhotoAddView.as_view(), name='comment-photo'),
    # groups
    path('groups/', GroupView.as_view(), name='groups'),
    path('group/<slug:slug>/', GroupDetail.as_view(), name='group-details'),
    path('group/<slug:slug>/add_post', GroupPostCreateView.as_view(), name='group-post'),
    path('group/<slug:slug>/append', GroupAppendView.as_view(), name='group-append'),
    path('create-group/', GroupCreateView.as_view(), name='create-group'),
    path('<str:username>/groups/', UsersGroupeView.as_view(), name='users-groups'),
    # messages
    path('messages/', MessagesView.as_view(), name='messages'),
    path('messages/<str:with_username>', MessagesWithUser.as_view(), name='messages-with-user'),

    path('api/groups/')
]
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
