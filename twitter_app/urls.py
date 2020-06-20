from django.urls import path
from . import views

urlpatterns = [
    path('api/tweet/', views.TweetListCreate.as_view() ),
    path('api/tweet/<int:pk>/', views.TweetRetrieveDestroy.as_view(), name='tweet_retrieve_delete' ),
    path('api/like/', views.LikeListCreate.as_view() ),
    path('api/like/<int:pk>/', views.LikeRetrieveDestroy.as_view(), name='like_retrieve_delete' ),
    path('api/profile/', views.ProfileListCreate.as_view(), name='profile_list_create' ),
    path('api/profile/<int:user>/', views.ProfileRetrieveUpdate.as_view(), name='profile_retrieve_update' ),
]
