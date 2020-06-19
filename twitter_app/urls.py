from django.urls import path
from . import views

urlpatterns = [
    path('api/tweet/', views.TweetListCreate.as_view() ),
    path('api/like/', views.LikeListCreate.as_view() ),
    path('api/like/<int:pk>/delete/', views.LikeDestroy.as_view(), name='like_delete' ),
]
