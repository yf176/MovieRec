from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from comment.forms import CommentForm
from comment.models import Comment
from user.models import MyUser
from .models import Movie
from rating.models import score
from django.core.cache import cache
from django.db.models import OuterRef, Subquery
from rec.rec import update_ml_movies


@login_required
def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    user = request.user
    rate = score.objects.filter(username=user.username, movieDataId=movie.dataId).first()
    comments = Comment.objects.filter(movieDataId=movie.dataId).order_by('-created_at')
    form = CommentForm()

    context = {
        'movie': movie,
        'comments': comments,
        'form': form,
    }

    if rate:
        context['rating'] = rate.score
    else:
        context['show_rating_button'] = True

    if request.method == 'POST':
        user_score = request.POST.get('score')
        if user_score:
            user_score = int(user_score)
            if 0 < user_score <= 10:
                rating = score.objects.create(username=user.username, movieDataId=movie.dataId, score=user_score)
                context['rating'] = rating.score
                context['show_rating_button'] = False
            update_ml_movies()

        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.username = request.user.username
            comment.movieDataId = movie.dataId
            comment.save()
            return redirect('movies:movie_detail', movie_id=movie.id)

    return render(request, 'movie_detail.html', context)


def rate(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    user = request.user

    # 判断用户是否已经对电影评分过
    rating = score.objects.filter(movieDataId=movie.dataId, username=user.username)
    if rating.exists():
        # 如果已经评分，则显示用户评分
        user_score = rating[0].score
        message = f'You rated {movie.title} with a score of {user_score}.'
    else:
        # 如果没有评分，则显示评分选项
        user_score = None
        message = f'Rate {movie.title}:'

        if request.method == 'POST':
            user_score = int(request.POST.get('score'))
            # 保存评分到数据库
            rating = score(username=user.username, movieDataId=movie.dataId, score=user_score)
            rating.save()
            message = f'You rated {movie.title} with a score of {user_score}.'
    movie_dataId = movie.dataId
    cache_key = f'mean_score_{movie_dataId}'
    cache.delete(cache_key)
    context = {
        'movie': movie,
        'score': user_score,
        'message': message,
    }
    return render(request, 'movie_detail.html', context)


def search(request):
    query = request.GET.get('query')
    movies = Movie.objects.filter(title__icontains=query)
    context = {
        'movies': movies,
        'query': query
    }
    return render(request, 'search.html', context)
