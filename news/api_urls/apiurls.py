from django.urls import path
from news.api_views import apiviews

urlpatterns = [
    path('posts/lists/', apiviews.PostsListAPIView.as_view()),
    path('posts/lists/draft/', apiviews.PostsDraftAPIView.as_view()),

    path('post/<slug:slug>/', apiviews.PostDetailAPIView.as_view()),
    path('posts/<str:category>/lists/', apiviews.PostCategoryAPIView.as_view()),
    path('posts/tag/<str:tag>/', apiviews.PostTagAPIView.as_view()),

    path('posts/create/', apiviews.PostCreateAPIView.as_view()),
    path('posts/update/<slug:slug>/', apiviews.PostUpdateAPIView.as_view()),
    path('posts/remove/<slug:slug>/', apiviews.PostDestroyAPIView.as_view()),

    path('comments/', apiviews.CommentListAPIView.as_view()),
    path('post/comments/<slug:slug>/', apiviews.PostCommentListCreateAPIView.as_view()),
    path('post/comments/update/<int:pk>/', apiviews.PostCommentUpdateAPIView.as_view()),
]
