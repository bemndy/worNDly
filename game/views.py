from django.db import models
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from datetime import date
import json
from .models import GameSession, Guess, DailyPlayCount
import random
from django.views.decorators.http import require_POST
from django.utils import timezone
from django.http import JsonResponse
from datetime import timedelta
from django.db.models import Count


from django.conf import settings
import os

MAX_FREE_GAMES_PER_DAY = 100
LANGUAGE_INFO = {
    'de': {'label': 'German'},
    'es': {'label': 'Spanish'},
    'fr': {'label': 'French'},
    'pt': {'label': 'Portuguese'},
    'en': {'label': 'English'},
}
WORDS_DIR = os.path.join(settings.BASE_DIR, 'words')
MAX_ATTEMPTS = 6


### HELPERS ###
def get_daily_record(user):
    today = date.today()
    obj, _ = DailyPlayCount.objects.get_or_create(user=user, date=today)
    return obj
def increment_daily_count(user):
    record = get_daily_record(user)
    record.count += 1
    record.save()

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




### Requests ###
def GameView(request):
    """Root game entry point — redirect to language select."""
    if not request.user.is_authenticated:
        return redirect('login')
    return redirect('language_select')


@login_required
def language_select(request):
    record = get_daily_record(request.user)
    free_remaining = max(0, MAX_FREE_GAMES_PER_DAY - record.count)

    now = timezone.now()
    period = request.GET.get('period', 'all')
    completed_games = GameSession.objects.filter(
        user=request.user,
        status__in=['won', 'lost'], # no active games
    )

    if period == 'week':
        completed_games = completed_games.filter(completed_at__gte=now - timedelta(weeks=1))
    elif period == 'month':
        completed_games = completed_games.filter(completed_at__gte=now - timedelta(days=30))
    elif period == 'year':
        completed_games = completed_games.filter(completed_at__gte=now - timedelta(days=365))

    completed_games = completed_games.order_by('-completed_at')
    total_played = completed_games.count()
    total_won    = completed_games.filter(status='won').count()
    win_rate     = round((total_won / total_played * 100)) if total_played else 0


    attempt_dist_qs = (
        completed_games
        .filter(status='won')
        .values('attempts_used')
        .annotate(total=Count('attempts_used'))
        .order_by() 
    )

    attempt_dict = {row['attempts_used']: row['total'] for row in attempt_dist_qs}
    attempt_dist_list = [attempt_dict.get(i, 0) for i in range(1, 7)]


    plays = []
    for game in completed_games:
        plays.append({
            'word':     game.target_word,
            'date':     game.completed_at.strftime('%b %d, %Y') if game.completed_at else '—',
            'passed':   game.status == 'won',
            'attempts': game.attempts_used,
        })


    return render(request, 'game/language_select.html', {
        'language_info': LANGUAGE_INFO,
        'played_today': record.count,
        'free_remaining': free_remaining,
        'max_free': MAX_FREE_GAMES_PER_DAY,
        'can_play': free_remaining > 0,
        # dashboard 1
        'period': period,
        'total_played': total_played,
        'total_won': total_won,
        'win_rate': win_rate,
        'attempt_dist_json':  json.dumps(attempt_dist_list),

        # dashboard 2
        'plays': plays,
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

    increment_daily_count(request.user)
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

@login_required
def buy_plays(request):
    record = get_daily_record(request.user)
    return render(request, 'game/buy_plays.html', {
        'played_today': record.count,
        'max_free': MAX_FREE_GAMES_PER_DAY,
    })


