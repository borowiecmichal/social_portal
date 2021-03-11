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
    PostCreateView, ProfileEditView
from social_portal import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', LandingView.as_view(), name='landing'),
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegistrationView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/<str:username>', UserProfileView.as_view(), name='user-profile'),
    path('add_photo/', PhotoCreateView.as_view(), name='add-photo'),
    path('add_post/', PostCreateView.as_view(), name='add-post'),
    path('profile/<str:username>/edit', ProfileEditView.as_view(), name='edit-user'),
]
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
