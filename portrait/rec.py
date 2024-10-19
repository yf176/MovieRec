from movies.models import Movie
from rating.models import score
from rec.rec import movieToArray, similarity
from user.models import MyUser


def portrait_rec(username, sorted_director_rank, sorted_writer_rank, sorted_tag_rank, sorted_actor_rank,
                 sorted_date_rank, sorted_country_rank):
    # 获取用户评分过的电影id列表
    rated_movies = score.objects.filter(username=username).values_list('movieDataId', flat=True)
    # 获取所有电影中未被当前用户评分的电影
    un_rated_movies = Movie.objects.exclude(dataId__in=rated_movies)
    # 初始化电影评分字典
    movie_scores = {}
    print(type(sorted_tag_rank))
    for movie in un_rated_movies:
        movie_scores[movie.dataId] = 0
        if movie.director and movie.director in sorted_director_rank:
            movie_scores[movie.dataId] += sorted_director_rank[movie.director]
        if movie.writer and movie.writer in sorted_writer_rank:
            movie_scores[movie.dataId] += sorted_writer_rank[movie.writer]
        if movie.tag1 and movie.tag1 in sorted_tag_rank:
            movie_scores[movie.dataId] += sorted_tag_rank[movie.tag1]
        if movie.tag2 and movie.tag2 in sorted_tag_rank:
            movie_scores[movie.dataId] += sorted_tag_rank[movie.tag2]
        if movie.tag3 and movie.tag3 in sorted_tag_rank:
            movie_scores[movie.dataId] += sorted_tag_rank[movie.tag3]
        if movie.actors:
            actor_list = movie.actors.split(' ')
            for actor in actor_list:
                if actor in sorted_tag_rank:
                    movie_scores[movie.dataId] += sorted_actor_rank[actor]
        if movie.country and movie.country in [m[0] for m in sorted_country_rank]:
            movie_scores[movie.dataId] += sorted_country_rank[movie.country]
    sorted_movie_scores = sorted(movie_scores.items(), key=lambda x: x[1], reverse=True)
    recommended_movie_dataIds = [m[0] for m in sorted_movie_scores][:10]
    return recommended_movie_dataIds
