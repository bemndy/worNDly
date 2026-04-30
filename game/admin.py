from django.contrib import admin
from .models import GameSession, Guess, UserPlayBank

# Register your models here.
admin.site.register(GameSession)
admin.site.register(Guess)
admin.site.register(UserPlayBank)
