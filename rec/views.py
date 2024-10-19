from django.shortcuts import render
from movies.models import Movie
from .rec import BICF, BUCF, coldstart  # 导入你的推荐算法


def recommendations(request):
    user_username = request.user.username
    recommended_movie_dataIds = coldstart(user_username)  # 获取推荐电影的 ID 列表
    recommended_movie_dataIds = list(set(recommended_movie_dataIds))
    recommended_movies = Movie.objects.filter(dataId__in=recommended_movie_dataIds)

    return render(request, 'recommendations.html', {'recommended_movies': recommended_movies})


def IBUCF(request):
    user_username = request.user.username
    recommended_movie_dataIds = BUCF(user_username)  # 获取推荐电影的 ID 列表
    recommended_movie_dataIds = list(set(recommended_movie_dataIds))
    recommended_movies = Movie.objects.filter(dataId__in=recommended_movie_dataIds)

    return render(request, 'IBUCF.html', {'recommended_movies': recommended_movies})


def IBICF(request):
    user_username = request.user.username
    recommended_movie_dataIds = BICF(user_username)  # 获取推荐电影的 ID 列表
    recommended_movie_dataIds = list(set(recommended_movie_dataIds))
    recommended_movies = Movie.objects.filter(dataId__in=recommended_movie_dataIds)

    return render(request, 'IBICF.html', {'recommended_movies': recommended_movies})