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

def post_detail(request, id):
    post = get_object_or_404(Post,
                             id=id,
                             status=Post.Status.PUBLISHED)
    return render(request, 'blog/detail.html', {'post': post})
