from django.urls import path
from apps.news.views import *


urlpatterns = [
    path('base/', basePageView, name='base-url'),
    path('', indexPageView, name='home'),
    path('category/<int:id>/', categoryPageView, name='category'),
    path('detail/<int:id>/', detailPageView, name='detail-blog'),
    path('comment/<int:id>/', commentPageView, name='comment-blog')
]


