from django.shortcuts import render
import os
from portrait.rec import portrait_rec
from rating.models import score
from movies.models import Movie
import matplotlib.pyplot as plt
from wordcloud import WordCloud


def analyse(request):
    username = request.user.username
    scores = score.objects.filter(username=username)
    director_rank = {}
    writer_rank = {}
    tag_rank = {}
    actor_rank = {}
    date_rank = {'1900-1950': 0, '1951-1980': 0, '1980-2000': 0, '2000-2012': 0, '2012-': 0}
    country_rank = {}

    for rec in scores:
        movie = Movie.objects.get(dataId=rec.movieDataId)
        if movie.rating == '':
            prefer = (float(rec.score) - 5.0) / 5.0
        else:
            prefer = (float(rec.score) - float(movie.rating)) / float(movie.rating)
        if movie.director != '':
            if movie.director not in director_rank:
                director_rank[movie.director] = prefer
            else:
                director_rank[movie.director] += prefer
        if movie.writer != '':
            if movie.writer not in writer_rank:
                writer_rank[movie.writer] = prefer
            else:
                director_rank[movie.director] += prefer
        if movie.tag1 != '':
            if movie.tag1 not in tag_rank:
                tag_rank[movie.tag1] = prefer
            else:
                tag_rank[movie.tag1] += prefer
        if movie.tag2 != '':
            if movie.tag2 not in tag_rank:
                tag_rank[movie.tag2] = prefer
            else:
                tag_rank[movie.tag2] += prefer
        if movie.tag3 != '':
            if movie.tag3 not in tag_rank:
                tag_rank[movie.tag3] = prefer
            else:
                tag_rank[movie.tag3] += prefer
        if movie.actors != '':
            actor_list = movie.actors.split(' ')
            for actor in actor_list:
                if actor not in actor_rank:
                    actor_rank[actor] = prefer
                else:
                    actor_rank[actor] += prefer
        if movie.country != '':
            if movie.country not in country_rank:
                country_rank[movie.country] = prefer
            else:
                country_rank[movie.country] += prefer
        if movie.date != '':
            date = float(movie.date)
            if date > 2012:
                date_rank['2012-'] += prefer
            elif date > 2000:
                date_rank['2000-2012'] += prefer
            elif date > 1980:
                date_rank['1980-2000'] += prefer
            elif date > 1950:
                date_rank['1951-1980'] += prefer
            else:
                date_rank['1900-1950'] += prefer
    sorted_director_rank = sorted(director_rank.items(), key=lambda x: x[1], reverse=True)
    sorted_writer_rank = sorted(writer_rank.items(), key=lambda x: x[1], reverse=True)
    sorted_tag_rank = sorted(tag_rank.items(), key=lambda x: x[1], reverse=True)
    sorted_actor_rank = sorted(actor_rank.items(), key=lambda x: x[1], reverse=True)
    sorted_date_rank = sorted(date_rank.items(), key=lambda x: x[1], reverse=True)
    sorted_country_rank = sorted(country_rank.items(), key=lambda x: x[1], reverse=True)
    recommended_movies = portrait_rec(username, director_rank, writer_rank, tag_rank,
                                      actor_rank,
                                      date_rank, country_rank)
    recommended_movie_dataIds = list(set(recommended_movies))
    recommended_movies = Movie.objects.filter(dataId__in=recommended_movie_dataIds)
    combined_dict = {**director_rank, **tag_rank, **writer_rank, **actor_rank, **date_rank, **country_rank}
    wordcloud = WordCloud(background_color='white', width=800, height=800, font_path='C:\\Users\\remnant\\Desktop'
                                                                                     '\\movierec\\static\\1.ttf')
    min_value = min(combined_dict.values())
    offset = abs(min_value)

    normalized_dict = {key: value + offset for key, value in combined_dict.items()}
    wordcloud.generate_from_frequencies(frequencies=normalized_dict)
    output_directory = 'static'
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    filename = f"{output_directory}/wordcloud_{username}.png"
    wordcloud.to_file(filename)
    # Generate the word cloud from the sorted_tag_rank dictionary
    context = {
        'director': sorted_director_rank[0][0] if sorted_actor_rank else '',
        'tag': sorted_tag_rank[0][0] if sorted_actor_rank else '',
        'writer': sorted_writer_rank[0][0] if sorted_writer_rank else '',
        'actor': sorted_actor_rank[0][0] if sorted_actor_rank else '',
        'date': sorted_date_rank[0][0] if sorted_date_rank else '',
        'country': sorted_country_rank[0][0] if sorted_country_rank else '',
        'recommended_movies': recommended_movies,
        'pic': f'/static/wordcloud_{username}.png'
    }
    return render(request, 'analyse.html', context)
