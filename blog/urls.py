from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='blog-home'),
    path('tag/<slug:tag_slug>/', views.home, name='home_by_tag'),
    # path('', views.PostListView.as_view(), name='blog-home'),
    path('about/', views.about, name='blog-about'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/',
    views.post_detail,
    name='post_detail'),
    path('<int:post_id>/share/', views.post_share, name='post_share'),
    path('<int:post_id>/comment/', views.post_comment, name='post_comment'),
]