from django.shortcuts import render
from .models import Post
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from .forms import EmailPostForm
from django.core.mail import send_mail

class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/home.html'

def home(request):
    post_list = Post.published.all()
    paginator = Paginator(post_list, 3)
    page_number = request.GET.get('page',1)
    try:
        posts = paginator.page(page_number)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        posts = paginator.page(1)
    context = {
        'posts' : posts
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

def post_share(request, post_id):
    post = get_object_or_404(
        Post,
        id=post_id,
        status=Post.Status.PUBLISHED
    )
    sent = False
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(
                post.get_absolute_url()
            )
            subject = (
                f"{cd['name']} ({cd['email']}) "
                f"recommends you read {post.title}"
            )
            message = (
                f"Read {post.title} at {post_url}\n\n"
                f"{cd['name']}\'s comments: {cd['comments']}"
            )
            send_mail(
                subject=subject,
                message = message,
                from_email=None,
                recipient_list=[cd['to']]
            )
            sent=True

            return render(
                request,
                'blog/share.html',
                {
                    'post': post,
                    'form': form,
                    'sent': sent
                }
            )
    
    else:
        form = EmailPostForm()
        return render(
            request,
            'blog/share.html',
            {
                'post': post,
                'form' : form,
                'sent' : sent
            }
        )
