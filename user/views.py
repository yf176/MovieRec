from django.contrib.auth.hashers import check_password
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
import datetime
from monitor.models import LoginRecord
from .models import MyUser
from rec.rec import update_ml_movies


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        # Check if passwords match
        if password1 != password2:
            error_message = 'Passwords do not match'
            return render(request, 'registration/register.html', {'error_message': error_message})

        # Check if username already exists
        if MyUser.objects.filter(username=username).exists():
            error_message = 'username already exists'
            return render(request, 'registration/register.html', {'error_message': error_message})

        # Create the user
        user = MyUser.objects.create_user(username=username, email=email, password=password1)
        user.save()

        # Log the user in and redirect to home page
        login(request, user)
        return render(request, 'registration/profile.html')

    return render(request, 'registration/register.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        try:
            user = MyUser.objects.get(username=username)
            if check_password(password, user.password):
                login(request, user)
                login_record = LoginRecord(username=user.username, login_time=datetime.datetime.now())
                login_record.save()
                if user.is_staff:
                    return redirect('monitor:add_movie')  # Replace with the URL name for the monitor's page
                else:
                    return redirect('user:profile')
            else:
                error_message = 'Invalid password'
                return render(request, 'registration/login.html', {'error_message': error_message})
        except MyUser.DoesNotExist:
            error_message = 'User does not exist'
            return render(request, 'registration/login.html', {'error_message': error_message})
    return render(request, 'registration/login.html')


def profile(request):
    update_ml_movies()
    return render(request, 'registration/profile.html')


def home(request):
    return render(request, 'registration/home.html')


def my_view(request):
    if request.method == 'POST' and 'logout' in request.POST:
        logout(request)
        return redirect('registration/logout.html')
    elif request.method == 'GET' and request.GET.get('logout'):
        logout(request)
        return redirect('registration/logout.html')


def logout_view(request):
    logout(request)
    return render(request, 'registration/logout.html')


def favourite(request):
    genres = ["爱情", "传记", "动画", "动作", "短片", "儿童", "犯罪", "歌舞", "古装", "纪录片", "家庭", "惊悚", "剧情", "科幻", "恐怖", "历史", "冒险",
              "奇幻", "脱口秀", "武侠", "舞台艺术", "西部", "喜剧", "悬疑", "音乐", "运动", "战争", "真人秀", "黑色电影", "情色", "同性", "灾难", "戏曲"]

    if request.method == 'POST':
        user = MyUser.objects.get(username=request.user.username)
        value_list = request.POST.getlist("movie_type", [])
        print(user.username)
        res = ""
        for i in value_list:
            res += i
            res += " "
        print(res)
        user.label = res
        user.save()
        return render(request, 'registration/favourite.html', {"select_value": value_list, "genres": genres})

    return render(request, 'registration/favourite.html', {"genres": genres})
