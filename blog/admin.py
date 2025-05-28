from django.contrib import admin
from .models import Category, Tag, Post, Comment

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at')
    search_fields = ('name',)
    ordering = ('-created_at',)

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1
    readonly_fields = ('created_at',)
    fields = ('author', 'content', 'approved', 'created_at')

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'is_published', 'views')
    list_filter = ('is_published', 'created_at', 'categories')
    search_fields = ('title', 'content')
    ordering = ('-created_at',)
    filter_horizontal = ('categories', 'tags')
    inlines = [CommentInline]
    readonly_fields = ('created_at', 'updated_at', 'views')
    prepopulated_fields = {'slug': ('title',)}

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'created_at', 'approved')
    list_filter = ('approved', 'created_at', 'post')
    search_fields = ('content', 'author__username', 'post__title')
    ordering = ('-created_at',)
    list_editable = ('approved',)
    readonly_fields = ('created_at',)
