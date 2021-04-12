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
from django.urls import path, include
from rest_framework import routers

from portal_app import views
from portal_app.views import LandingView, LoginView, LogoutView, UserProfileView, PhotoCreateView, \
    PostCreateView, ProfileEditView, CommentToPostAddView, GroupView, GroupDetail, GroupPostCreateView, GroupAppendView, \
    GroupCreateView, UsersGroupeView, CommentToPhotoAddView, MessagesView, MessagesWithUser, LikePostView, \
    UserRegistrationView, GroupeDelete, GroupeRequests, GroupeRequestsAcceptUser, GroupeRequestsRejectUser, GroupeLeave, \
    LikeView
from social_portal import settings
from django.contrib.auth import views as auth_views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),  # test done
    path('', LandingView.as_view(), name='home'),
    path('login/', LoginView.as_view(), name='login'),  # test done
    path('register/', UserRegistrationView.as_view(), name='register'),  # test done
    path('logout/', LogoutView.as_view(), name='logout'),  # test done
    path('profile/<str:username>', UserProfileView.as_view(), name='user-profile'),  # test done
    path('add_photo/', PhotoCreateView.as_view(), name='add-photo'),  # test omitted
    path('add_post/', PostCreateView.as_view(), name='add-post'),  # test done
    path('like-post/<int:post_id>/', LikePostView.as_view(), name='like-post'),  # test done
    path('profile/<str:username>/edit', ProfileEditView.as_view(), name='edit-user'),  # test done
    path(
        'change-password/',
        auth_views.PasswordChangeView.as_view(
            template_name='commons/change-password.html',
            success_url='/'
        ),
        name='change_password'
    ),
    path('comment-post/<int:post_id>', CommentToPostAddView.as_view(), name='comment-post'),  # test done
    path('comment-photo/<int:photo_id>', CommentToPhotoAddView.as_view(), name='comment-photo'),  # test omitted
    # groups
    path('groups/', GroupView.as_view(), name='groups'),  # test done
    path('group/<slug:slug>/', GroupDetail.as_view(), name='group-details'),  # test done
    path('group/<slug:slug>/add_post/', GroupPostCreateView.as_view(), name='group-post'),  # test done
    path('group/<slug:slug>/append', GroupAppendView.as_view(), name='group-append'),  # test done
    path('create-group/', GroupCreateView.as_view(), name='create-group'),  # test done
    path('<str:username>/groups/', UsersGroupeView.as_view(), name='users-groups'),  # test done
    path('groups/delete/<slug:slug>/', GroupeDelete.as_view(), name='group-delete'),  # test done
    path('groups/requests-users/<slug:slug>/', GroupeRequests.as_view(), name='group-requests'),
    path('groups/requests-users/<slug:slug>/accept/<str:username>/', GroupeRequestsAcceptUser.as_view(),
         name='group-user-accept'),  # test done
    path('groups/requests-users/<slug:slug>/reject/<str:username>/', GroupeRequestsRejectUser.as_view(),
         name='group-user-reject'),  # test done
    path('groups/leave/<slug:slug>/', GroupeLeave.as_view(), name='group-leave'),  # test done

    # messages
    path('messages/', MessagesView.as_view(), name='messages'),  # test done
    path('messages/<str:with_username>', MessagesWithUser.as_view(), name='messages-with-user'),  # test done

    # API
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('like/', LikeView.as_view(), name='like'),

]
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
