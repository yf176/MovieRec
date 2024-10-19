from django.urls import path
from api.views import user_list
from .views import register, login_view, home, profile, logout_view, favourite
from django.contrib.auth import views as auth_views

app_name = 'user'

urlpatterns = [
    path('home/', home, name='home'),
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('api/user_list/', user_list, name='user_list'),
    path('profile/', profile, name='profile'),
    path('logout/', logout_view, name='logout'),
    path('favouriate/', favourite, name='favourite'),
]
