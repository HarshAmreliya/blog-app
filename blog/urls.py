from django.urls import path
from . import views

urlpatterns = [
    path('', views.PostListView.as_view(), name='blog-home'),
    path('about/', views.about, name='blog-about'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/',
    views.post_detail,
    name='post_detail'),
]