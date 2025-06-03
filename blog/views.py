from django.shortcuts import render
from .models import Post
from django.shortcuts import get_object_or_404

def home(request):
    context = {
        'posts' : Post.published.all()
    }
    return render(request, 'blog/home.html', context)

def about(request):
    return render(request, 'blog/about.html', {'title':'About'})

def post_detail(request, year, day, month, post):
    post = get_object_or_404(Post,
                             status=Post.Status.PUBLISHED,
                             slug=post,
                             date_posted__year=year,
                             date_posted__month=month,
                             date_posted__day=day
                             )
    return render(request, 'blog/detail.html', {'post': post})
