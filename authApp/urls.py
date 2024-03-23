
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from authApp import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('social-auth', include('social_django.urls', namespace='social')),
    path("authhome/", views.home, name='home'),
    path('signup/',views.signup,name='signup'),
]
