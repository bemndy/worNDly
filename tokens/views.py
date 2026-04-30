import os

from django.shortcuts import render, redirect
import requests
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from game.views import get_daily_record

# Create your views here.

ACCESS_TOKEN = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzg2MTQzODkzLCJpYXQiOjE3Nzc1MDM4OTMsImp0aSI6IjZjOGUwMGFhNGJmNDQzOTFiOTA5MTQ3Nzc1ZjY1MTMwIiwidXNlcl9pZCI6NTN9.8dsiReyLVmDlGVWW8VQulBfgvxYwpsphCHRtQJ1LFCc'
@login_required
def BuyTokensView(request):
    return render(request, 'tokens/token_balance.html', {
        'players': view_all_coins(ACCESS_TOKEN),
        'current_player': view_balance_for_user(
            ACCESS_TOKEN, 
            request.user.email)
    })

def view_all_coins(access_token):
   # Use the access token to make an authenticated request
   headers = {
       'Authorization': f'Bearer {access_token}'
   }


   # Make a GET request with the authorization header
   api_response = requests.get("https://jcssantos.pythonanywhere.com/api/group22/group22/", headers=headers)


   if api_response.status_code == 200:
       # Process the data from the API
       return api_response.json()
   else:
       print("Failed to access the API endpoint to view all coins:", api_response.status_code)

def view_balance_for_user(access_token, email):
   # Use the access token to make an authenticated request
   headers = {
       'Authorization': f'Bearer {access_token}'
   }


   # Make a GET request with the authorization header
   api_response = requests.get(f"https://jcssantos.pythonanywhere.com/api/group22/group22/player/{email}/", headers=headers)


   if api_response.status_code == 200:
       return api_response.json()
   elif api_response.status_code == 404:
       return user_initialize_balance(access_token, email)
   else:
       print("Failed to access the API endpoint to view balance for user:", api_response.status_code)

@login_required
@require_POST
def buy_play(request):
    email = request.user.email
    quantity = int(request.POST.get('quantity', 1))
    result = user_pay(ACCESS_TOKEN, email, quantity)

    context = {
        'players': view_all_coins(ACCESS_TOKEN),
        'current_player': view_balance_for_user(ACCESS_TOKEN, email),
    }

    if result is None:
        context['error'] = 'Purchase failed. Check your token balance.'
    else:
        record = get_daily_record(request.user)
        record.purchased += quantity
        record.save()
        context['success'] = f'Successfully purchased {quantity} play(s)!'

    return render(request, 'tokens/token_balance.html', context)

def user_pay(access_token, email, amount):
   # Use the access token to make an authenticated request
   headers = {
       'Authorization': f'Bearer {access_token}'
   }
   data = {"amount": amount} # non-negative integer value to be decreased
   # Make a POST request with the authorization header and data payload
   api_response = requests.post(f"https://jcssantos.pythonanywhere.com/api/group22/group22/player/{email}/pay", headers=headers, data=data)


   if api_response.status_code == 200:
       # Process the data from the API
       return api_response.json()
   else:
       print("Failed to access the API endpoint to pay:", api_response.status_code)

def user_initialize_balance(access_token, email):
   # Use the access token to make an authenticated request
   headers = {
       'Authorization': f'Bearer {access_token}'
   }
   data = {"amount": 20} # Initialize with zero tokens
   # Make a POST request with the authorization header and data payload to add a user
   api_response = requests.post(f"https://jcssantos.pythonanywhere.com/api/group22/group22/player/add", headers=headers, data=data)


   if api_response.status_code == 200:
       # Process the data from the API
       return api_response.json()
   else:
       print("Failed to access the API endpoint to initialize balance:", api_response.status_code)