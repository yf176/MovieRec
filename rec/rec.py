import copy
import time
from functools import lru_cache, wraps

from django.db.models import Count, Q, Avg, OuterRef, Subquery

from user.models import MyUser
from movies.models import Movie
from rating.models import score
import numpy as np


# time装饰器
def timer(func):
    @wraps(func)
    def wrap(*args, **kwargs):
        begin_time = time.perf_counter()
        result = func(*args, **kwargs)
        start_time = time.perf_counter()
        print('func:%r args:[%r, %r] took: %2.4f sec' % (func.__name__, args, kwargs, start_time - begin_time))
        return result

    return wrap


genres = ["爱情", "传记", "动画", "动作", "短片", "儿童", "犯罪", "歌舞", "古装", "纪录片", "家庭", "惊悚", "剧情", "科幻", "恐怖", "历史", "冒险",
          "奇幻", "脱口秀", "武侠", "舞台艺术", "西部", "喜剧", "悬疑", "音乐", "运动", "战争", "真人秀", "黑色电影", "情色", "同性", "灾难", "戏曲"]
genres_array=[0 for i in range(len(genres))]

def movieToArray(movie, genres):
    movie_array = copy.deepcopy(genres_array)
    if movie.tag1 in genres:
        p1 = genres.index(movie.tag1)
        movie_array[p1] = 1
    if movie.tag2 in genres:
        p2 = genres.index(movie.tag2)
        movie_array[p2] = 1
    if movie.tag3 in genres:
        p3 = genres.index(movie.tag3)
        movie_array[p3] = 1
    return movie_array


def get_dataID():
    ms = Movie.objects.values('dataId').order_by('dataId')
    ml = [data['dataId'] for data in ms]
    return ml


@lru_cache(1024)
def get_movie_mean_score(movie_dataId):
    mean_i = score.objects.filter(movieDataId=movie_dataId).aggregate(mean_score=Avg('score'))['mean_score']
    return mean_i


ml = get_dataID()


def get_all_movie_score_dict():
    d = {}
    for m in ml:
        score = get_movie_mean_score(m)
        d[m] = score
    return d


movie_score_dict = get_all_movie_score_dict()


@lru_cache(32)
def get_user_rating(username):
    user_ratings = score.objects.filter(username=username).values_list('movieDataId', flat=True)
    return user_ratings


@lru_cache(1024)
def get_user_vec(username):
    vec = [0] * len(ml)
    scores = score.objects.filter(username=username, movieDataId__in=ml)
    for s in scores:
        try:
            index = ml.index(s.movieDataId)
            if index:
                vec[index - 1] = 1
        except Exception as e:
            print(e.args)
    return vec


def get_all_movies():
    movie_dict = {}
    movie_arr_dict = {}
    movies = Movie.objects.all()
    for movie in movies:
        movie_dict[movie.dataId] = movie
        movie_arr_dict[movie.dataId] = movieToArray(movie, genres)
    return movie_dict, movie_arr_dict


movie_dict, movie_arr_dict = get_all_movies()


def update_ml_movies():
    global ml
    ml = get_dataID()
    global movie_score_dict
    movie_score_dict = get_all_movie_score_dict()
    global movie_dict
    movie_dict, movie_arr_dict = get_all_movies()


@timer
def BICF(username, n=10):
    # 获取用户评分过的电影id列表
    rated_movies_dataId = get_user_rating(username)
    # 初始化电影评分字典
    movie_scores = {}
    # 获取用户评分过的电影平均相似度(RBICF)
    for dataId in ml:
        if dataId in rated_movies_dataId:
            continue
        movie_unrated = movie_dict.get(dataId, None)
        if movie_unrated is None:
            continue
        rbicf = 0
        mean_i = movie_score_dict.get(dataId, None)
        if mean_i is None and movie_unrated.rating != '':
            mean_i = float(movie_unrated.rating)
        else:
            mean_i = 0
        cur_un_rate_arr = movie_arr_dict.get(dataId, None)
        for rated_id in rated_movies_dataId:
            movie_rated = movie_score_dict.get(rated_id, None)
            if movie_rated is None:
                continue
            cur_rate_arr = movie_arr_dict.get(rated_id, None)
            rbicf += float(similarity(cur_rate_arr, cur_un_rate_arr))
        movie_scores[dataId] = rbicf * mean_i

    # 返回前n个电影
    sorted_movie_scores = sorted(movie_scores.items(), key=lambda x: x[1], reverse=True)
    recommended_movie_dataIds = [m[0] for m in sorted_movie_scores][:10]
    print(sorted_movie_scores)
    return recommended_movie_dataIds


@timer
def BUCF(username, n=10):
    # 获取用户的评分向量
    user_vector = get_user_vec(username)
    # 获取和当前用户相似的用户列表
    user_ratings = get_user_rating(username)
    if user_ratings is None:
        return []
    similarity_subquery = score.objects.filter(username=OuterRef('username'), movieDataId__in=user_ratings).values(
        'username').annotate(similarity=Count('id')).values('similarity')
    similar_users = MyUser.objects.filter(~Q(username=username)).annotate(
        similarity=Subquery(similarity_subquery)).order_by('-similarity')[:n]
    # 初始化电影评分字典
    movie_scores = {}
    # 遍历相似用户
    print(similar_users)
    for sim_user in similar_users:
        # 获取相似用户的评分向量
        sim_user_vector = get_user_vec(sim_user)
        # 获取和当前用户的差异向量
        diff_vector = [sim_user_vector[i] - user_vector[i] for i in range(len(user_vector))]
        # 获取相似用户和当前用户都没有评分过的电影列表
        un_rated_movies = [ml[i] for i in range(len(user_vector)) if user_vector[i] == 0]
        # 计算当前相似用户对这些电影的兴趣度，并考虑mean(i)
        for movie_dataId in un_rated_movies:
            mean_i = movie_score_dict.get(movie_dataId, None)
            if mean_i is None:
                mean_i = 0
            if movie_dataId in movie_scores:
                if sim_user.similarity is None:
                    movie_scores[movie_dataId] += 0
                else:
                    movie_scores[movie_dataId] += sim_user.similarity * diff_vector[ml.index(movie_dataId)] * mean_i
            else:
                if sim_user.similarity is None:
                    movie_scores[movie_dataId] = 0
                movie_scores[movie_dataId] = sim_user.similarity * diff_vector[ml.index(movie_dataId)] * mean_i
    # 将电影兴趣度按降序排列
    sorted_movie_scores = sorted(movie_scores.items(), key=lambda x: x[1], reverse=True)
    # print(diff_vector)
    # 获取推荐电影的id列表
    recommended_movie_dataIds = [m[0] for m in sorted_movie_scores][:n]
    print(sorted_movie_scores)
    return recommended_movie_dataIds


def coldstart(username):
    genres = ["爱情", "传记", "动画", "动作", "短片", "儿童", "犯罪", "歌舞", "古装", "纪录片", "家庭", "惊悚", "剧情", "科幻", "恐怖", "历史", "冒险",
              "奇幻", "脱口秀", "武侠", "舞台艺术", "西部", "喜剧", "悬疑", "音乐", "运动", "战争", "真人秀", "黑色电影", "情色", "同性", "灾难", "戏曲"]
    user = MyUser.objects.get(username=username)
    tags = user.label
    tag_array = tags.split(" ")
    bi_array = []
    # 获取用户向量
    for i in genres:
        if i in tag_array:
            bi_array.append(1)
        else:
            bi_array.append(0)
    print(bi_array)
    # 获取用户评分过的电影id列表
    rated_movies = score.objects.filter(username=username).values_list('movieDataId', flat=True)
    # 获取所有电影中未被当前用户评分的电影
    un_rated_movies = Movie.objects.exclude(dataId__in=rated_movies)
    # 初始化电影评分字典
    movie_scores = {}
    for movie in un_rated_movies:
        if movie.rating != '':
            movie_array = movieToArray(movie, genres)
            movie_scores[movie.dataId] = float(similarity(movie_array, bi_array)) * float(movie.rating)
            print(similarity(movie_array, bi_array))
            print(similarity(movie_array, bi_array))
    sorted_movie_scores = sorted(movie_scores.items(), key=lambda x: x[1], reverse=True)
    recommended_movie_dataIds = [m[0] for m in sorted_movie_scores][:10]
    return recommended_movie_dataIds


# 这个BUCF算法主要实现以下功能：

#  获取用户已评分的电影列表。
# 获取未被当前用户评分的电影列表。
# 找到与当前用户相似的其他用户列表。
# 计算这些相似用户评分过但当前用户未评分的电影的兴趣度。
# 返回兴趣度最高的前n个电影作为推荐结果。


def similarity(u, v):
    return np.dot(u, v) + 1 / (np.linalg.norm(u) * np.linalg.norm(v) + 1)
