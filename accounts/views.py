from django.shortcuts import render
from django.contrib.auth.models import User

# Create your views here.

def RegisterView(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        if not username:
            username = 'no_username' # default username if not provided
        password = request.POST.get('password')
        email = request.POST.get('email')

        # create the user object and save it to the database
        user = User.objects.create_user(username=username, password=password, email=email)
        user.save()
        return render(request, 'accounts/login.html', {'success': 'Registration successful. Please log in to verify.'})
    return render(request, 'accounts/register.html')