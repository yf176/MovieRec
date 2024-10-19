from django.urls import path
from . import views

app_name = 'movies'

urlpatterns = [
    path('movie_detail/<int:movie_id>/', views.movie_detail, name='movie_detail'),
    path('search/', views.search, name='search'),
    path('rate/<int:movie_id>/', views.rate, name='rate'),
]