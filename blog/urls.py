from django.urls import path

from blog.views import PostDetailView, PostListView


app_name = 'blog'
urlpatterns = [
    path('', PostListView.as_view(), name='post_list'),
    path('post/<int:post_pk>/<slug:post_slug>/', PostDetailView.as_view(), name='post_detail'),
]