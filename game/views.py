from django.db import models
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from datetime import date
import json
from .models import GameSession, Guess
import random
from django.views.decorators.http import require_POST
from django.utils import timezone
from django.http import JsonResponse


from django.conf import settings
import os

MAX_FREE_GAMES_PER_DAY = 3
LANGUAGE_INFO = {
    'de': {'label': 'German'},
    'es': {'label': 'Spanish'},
    'fr': {'label': 'French'},
    'pt': {'label': 'Portuguese'},
    'en': {'label': 'English'},
}
WORDS_DIR = os.path.join(settings.BASE_DIR, 'words')
MAX_ATTEMPTS = 6


def get_word_list(language):
    filepath = os.path.join(WORDS_DIR, f'{language}.txt')
    if not os.path.exists(filepath):
        print('path not found')
        return []
    with open(filepath, 'r', encoding='utf-8') as f:
        words = [line.strip().lower() for line in f]
    return words

def evaluate_guess(guess_word, target_word):
    """
    Returns list of 'correct' | 'present' | 'absent' for each letter.
    Handles duplicate letters correctly.
    """
    result = ['absent'] * 5
    target = list(target_word)
    guess  = list(guess_word)

    for i in range(5):
        if guess[i] == target[i]:
            result[i] = 'correct'
            target[i] = None
            guess[i]  = None 

    # Pass 2: mark present letters
    for i in range(5):
        if guess[i] is not None and guess[i] in target:
            result[i] = 'present'
            target[target.index(guess[i])] = None


    print(result)
    return result



def GameView(request):
    """Root game entry point — redirect to language select."""
    if not request.user.is_authenticated:
        return redirect('login')
    return redirect('language_select')

def get_daily_record(user):
    today = date.today()
    # obj, _ = DailyPlayCount.objects.get_or_create(user=user, date=today)
    # return obj



@login_required
def language_select(request):
    # record = get_daily_record(request.user)
    # free_remaining = max(0, MAX_FREE_GAMES_PER_DAY - record.count)
    # return render(request, 'game/language_select.html', {
    #     'language_info': LANGUAGE_INFO,
    #     'played_today': record.count,
    #     'free_remaining': free_remaining,
    #     'max_free': MAX_FREE_GAMES_PER_DAY,
    #     'can_play': free_remaining > 0,
    # })
    return render(request, 'game/language_select.html', {
        'language_info': LANGUAGE_INFO,
        'played_today': 0,
        'free_remaining': 3,
        'max_free': MAX_FREE_GAMES_PER_DAY,
        'can_play': 3 > 0,
    })


@login_required
def start_game(request, language):

    words = get_word_list(language)
    chosen_word = random.choice(words)

    game = GameSession.objects.create(
        user=request.user,
        language=language,
        target_word=chosen_word,
    )
    return redirect('play_game', game_id=game.id)

@login_required
def play_game(request, game_id):
    game = get_object_or_404(GameSession, id=game_id, user=request.user)
    guesses = list(game.guess_set.all())
    word_list = get_word_list(game.language)


    lang = LANGUAGE_INFO.get(game.language, {})

    return render(request, 'game/game.html', {
        'game': game,
        'guesses_json': json.dumps([{'word': g.word, 'result': g.result} for g in guesses]),
        'max_attempts': MAX_ATTEMPTS,
        # 'lang_label': lang.get('label', game.language),
        # 'lang_flag': lang.get('flag', ''),
        'word_list_json': json.dumps(word_list),
    })


@login_required
@require_POST
def submit_guess(request, game_id):
    game = get_object_or_404(GameSession, id=game_id, user=request.user)
    if game.status != 'active':
        return JsonResponse({'error': 'Game is already over.'}, status=400)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid request.'}, status=400)

    guess_word = data.get('word', '').strip().lower()

    if len(guess_word) != 5:
        return JsonResponse({'error': 'Word must be exactly 5 letters.'}, status=400)

    if not guess_word.isalpha():
        return JsonResponse({'error': 'Word must contain only letters.'}, status=400)

    word_list = get_word_list(game.language)
    if guess_word not in word_list:
        return JsonResponse({'error': f'"{guess_word.upper()}" is not in the word list.'}, status=400)

    attempt_number = game.attempts_used + 1
    result = evaluate_guess(guess_word, game.target_word)

    Guess.objects.create(
        game=game,
        attempt_number=attempt_number,
        word=guess_word,
        result=result,
    )

    game.attempts_used = attempt_number
    won = all(r == 'correct' for r in result)
    game_over = won or attempt_number >= MAX_ATTEMPTS

    if won:
        game.status = 'won'
        game.completed_at = timezone.now()
    elif attempt_number >= MAX_ATTEMPTS:
        game.status = 'lost'
        game.completed_at = timezone.now()

    game.save()


    return JsonResponse({
        'result': result,
        'word': guess_word,
        'attempt_number': attempt_number,
        'won': won,
        'game_over': game_over,
        'target_word': game.target_word if game_over else None,
        'status': game.status,
    })

