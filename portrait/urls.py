from django.urls import path
from . import views

app_name = 'portrait'

urlpatterns = [
    path('analyse/', views.analyse, name='analyse'),
]