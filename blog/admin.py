from django.contrib import admin
from .models import Comment, Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'author', 'date_posted', 'status']
    list_filter = ['status', 'date_created', 'date_posted', 'author']
    search_fields = ['title', 'body']
    raw_id_fields = ['author']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'date_posted'
    ordering = ['status', 'date_posted']
    show_facets = admin.ShowFacets.ALWAYS

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'post', 'created', 'active']
    list_filter = ['active', 'created', 'updated']
    search_fields = ['name', 'email', 'body']