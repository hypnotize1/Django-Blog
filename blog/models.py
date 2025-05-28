from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Post(models.Model):
    objects = None
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    is_published = models.BooleanField(default=False)
    views = models.IntegerField(default=0)
    categories = models.ManyToManyField(Category, related_name='posts')
    tags = models.ManyToManyField(Tag, related_name='posts')
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ['-created_at']

    def get_absolute_url(self):
        return reverse('blog:post_detail', kwargs={'post_pk': self.pk, 'post_slug': self.slug})

    def __str__(self):
        return self.title



class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_comments')
    content = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def approve(self):
        self.approved = True
        self.save()

    def get_absolute_url(self):
        return self.post.get_absolute_url()

    def __str__(self):
        return f'Comment by {self.author.username} on {self.post.title}'
