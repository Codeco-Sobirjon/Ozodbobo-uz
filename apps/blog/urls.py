from django.urls import path
from apps.blog.views import *


urlpatterns = [
    path('categories/', CategoriesListCreateAPIView.as_view(), name='categories-list-create'),
    path('category/<int:pk>/', CategoriesDetailAPIView.as_view(), name='categories-detail'),

    path('blog/<int:pk>/', BlogDetailView.as_view()),
    path('blogs/<int:pk>/', BlogListView.as_view()),

    path('carousel/<int:pk>/', CarouselBlogListView.as_view()),

    path('popular/<int:pk>/', PopularBlogListView.as_view()),

    path("comment/post/", BlogCommentCreateView.as_view())

]