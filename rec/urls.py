from django.urls import path
from . import views

app_name = 'rec'

urlpatterns = [
    path('recommendations/', views.recommendations, name='recommendations'),
    path('IBUCF/', views.IBUCF, name='IBUCF'),
    path('IBICF/', views.IBICF, name='IBICF'),
]