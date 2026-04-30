from django.db import models
from django.contrib.auth.models import User


class GameSession(models.Model):
    LANGUAGE_CHOICES = [
        ('en', 'English'),
        ('es', 'Spanish'),
        ('fr', 'French'),
        ('de', 'German'),
        ('pt', 'Portuguese'),
    ]
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('won', 'Won'),
        ('lost', 'Lost'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    language = models.CharField(max_length=2, choices=LANGUAGE_CHOICES)
    target_word = models.CharField(max_length=5)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    attempts_used = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.target_word} {self.status} {self.attempts_used}"

class Guess(models.Model):
    game = models.ForeignKey(GameSession, on_delete=models.CASCADE, related_name='guess_set')
    attempt_number = models.IntegerField()
    word = models.CharField(max_length=5)
    result = models.JSONField()  # list of 'correct' | 'present' | 'absent'

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['game', 'attempt_number'],
                name='unique_game_attempt'
            )
        ]
    def __str__(self):
        return f"Game {self.game.id} | Attempt {self.attempt_number}: {self.word}"
    

class UserPlayBank(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='play_bank')
    plays_remaining = models.IntegerField(default=0)
    last_reset = models.DateField()

    def __str__(self):
        return f"{self.user.username} | {self.plays_remaining} plays remaining"


