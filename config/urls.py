"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect
from game import views as game_views
from accounts import views as accounts_views

# Using the redirect in game/views.py to check AUTH status and redirect to login if not logged in
# Also using it for the "" root URL to redirect to /game if logged in, or /login if not logged in 

def home(request):
    if request.user.is_authenticated:
        return redirect('game')
    return redirect('login')

urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls),
    path('game/', game_views.GameView, name='game'),
    path('login/', LoginView.as_view(
        template_name='accounts/login.html', 
        next_page='/game/',
        redirect_authenticated_user=True
    ), name='login'),
    path('logout/', LogoutView.as_view(
        template_name='accounts/logout.html',
    ), name='logout'),
    path('signup/', accounts_views.RegisterView, name='signup'),
]