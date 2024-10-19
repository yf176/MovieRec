from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from rest_framework.generics import get_object_or_404

from portrait.rec import portrait_rec
from rating.models import score
from movies.models import Movie
from django.core.cache import cache
from django.db.models import OuterRef, Subquery
from rec.rec import update_ml_movies


@login_required
def rating(request):
    username = request.user.username
    scores = score.objects.filter(username=username)
    res = []
    for rec in scores:
        movie = Movie.objects.filter(dataId=rec.movieDataId)
        if movie.exists():
            res.append([movie[0].title, rec.score])
        res = [i for n, i in enumerate(res) if i not in res[:n]]
    update_ml_movies()
    context = {
        'scores': res,
    }
    return render(request, 'rating.html', context)


def rate_movie(request, movie_dataId, user_rating):
    # ... Code to save the user rating ...

    # Invalidate the mean score cache for the rated movie
    cache_key = f'mean_score_{movie_dataId}'
    cache.delete(cache_key)
