from django.conf import settings
from django.contrib import admin
from django.contrib.auth import views
from django.urls import path, include

from .views import AccessView, ProfileView, ChangePasswordView

urlpatterns = [

    path('', AccessView.as_view(), name='access'),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("password/change/", ChangePasswordView.as_view(), name="password-change"),
]
