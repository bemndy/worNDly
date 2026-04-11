from django.shortcuts import render
from django.contrib.auth.models import User

# Create your views here.

def RegisterView(request):
    if request.method == 'POST':
        name = request.POST.get('name', '')       # optional
        username = request.POST.get('username', '')
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')

        # validate required fields
        if not username or not email or not password:
            return render(request, 'accounts/register.html', {'error': 'Username, email, and password are required.'})

        if User.objects.filter(username=username).exists():
            return render(request, 'accounts/register.html', {'error': 'Username already taken.'})

        # create the user object and save it to the database
        user = User.objects.create_user(username=username, password=password, email=email)
        user.first_name = name  # optional name field
        user.save()
        return render(request, 'accounts/login.html', {'success': 'Registration successful. Please log in.'})
    return render(request, 'accounts/register.html')