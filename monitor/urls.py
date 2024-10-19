from django.urls import path
from . import views

app_name = 'monitor'

urlpatterns = [
    path('login_records/', views.login_records, name='login_records'),
    path('add_movie/', views.add_movie, name='add_movie'),
    path('comment_records/', views.comment_records, name='comment_records'),
]
