from django.urls import path
from . import views

app_name = 'rating'

urlpatterns = [
    path('rating/', views.rating, name='rating'),
]