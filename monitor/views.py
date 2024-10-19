from django.shortcuts import render, redirect
from movies.models import Movie
from .forms import MovieForm
from .models import LoginRecord
from comment.models import Comment

def add_movie(request):
    tags = ["爱情", "传记", "动画", "动作", "短片", "儿童", "犯罪", "歌舞", "古装", "纪录片", "家庭", "惊悚", "剧情", "科幻", "恐怖", "历史", "冒险", "奇幻",
            "脱口秀", "武侠", "舞台艺术", "西部", "喜剧", "悬疑", "音乐", "运动", "战争", "真人秀", "黑色电影", "情色", "同性", "灾难", "戏曲"]
    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('monitor:add_movie')  # Replace with the URL name for the monitor's page
    else:
        form = MovieForm()
    return render(request, 'add_movie.html', {'form': form, 'tags': tags})


def login_records(request):
    records = LoginRecord.objects.all().order_by('-login_time')
    return render(request, 'login_records.html', {'records': records})


def comment_records(request):
    comments = Comment.objects.all().order_by('-created_at')
    comment_movie_list = []
    for comment in comments:
        movie = Movie.objects.get(dataId=comment.movieDataId)
        comment_movie_list.append((comment, movie))
    context = {'comment_movie_list': comment_movie_list}
    return render(request, 'comment_records.html', context)

