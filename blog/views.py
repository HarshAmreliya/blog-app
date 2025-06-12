from django.shortcuts import render
from .models import Post
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from .forms import EmailPostForm, CommentForm
from django.core.mail import send_mail
from django.views.decorators.http import require_POST
from taggit.models import Tag
from django.db.models import Count

class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/home.html'

def home(request, tag_slug=None):
    post_list = Post.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        post_list = post_list.filter(tags__in=[tag])
    paginator = Paginator(post_list, 3)
    page_number = request.GET.get('page',1)
    try:
        posts = paginator.page(page_number)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        posts = paginator.page(1)
    context = {
        'posts' : posts,
        'tag' : tag
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
    comments = post.comments.filter(active=True)
    form = CommentForm()
    #List of similar posts
    post_tags_ids = post.tags.values_list('id', flat=True)
    # post_tags_list = post.tags.values_list('name', flat=True)
    similar_posts = Post.published.filter(
        tags__in=post_tags_ids
    ).exclude(id=post.id)
    similar_posts = similar_posts.annotate(
        same_tags=Count('tags')
    ).order_by('-same_tags', '-date_posted')[:4]
    return render(
        request, 'blog/detail.html', {
        'post': post,
        'comments' : comments,
        'form' : form,
        'similar_posts' : similar_posts
        # 'post_tags_list' : post_tags_list
        }
    )

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
    
@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(
        Post,
        id=post_id,
        status=Post.Status.PUBLISHED
    )
    comment = None
    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
        return render(
            request,
            'blog/comment.html',
            {
                'post' : post,
                'form' : form,
                'comment' : comment
            }
        )
