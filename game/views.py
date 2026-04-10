from django.shortcuts import render, redirect
from django.contrib.auth import authenticate

# Create your views here.

def GameView(request):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        return render(request, 'game/game.html')
