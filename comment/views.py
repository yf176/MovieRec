from django.shortcuts import get_object_or_404, redirect, render

from movies.models import Movie
from comment.models import Comment
from .forms import CommentForm

def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    comments = Comment.objects.filter(movieDataId=movie.dataId).order_by('-created_at')
    form = CommentForm()

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.username = request.user.username
            comment.movieDataId = movie.dataId
            comment.save()
            return redirect('movies:movie_detail', movie_id=movie.id)

    context = {
        'movie': movie,
        'comments': comments,
        'form': form,
    }
    return render(request, 'movie_detail.html', context)
