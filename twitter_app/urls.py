from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token

from . import views
from .views import current_user, UserList

urlpatterns = [
    path('api/tweet/', views.TweetListCreate.as_view() ),
    path('api/tweet/<int:pk>/', views.TweetRetrieveDestroy.as_view(), name='tweet_retrieve_delete' ),
    path('api/tweet/author/<int:author>/', views.TweetListByAuthor.as_view(), name='tweet_retrieve_delete'),
    path('api/like/', views.LikeListCreate.as_view() ),
    path('api/like/<int:tweet>/', views.LikeRetrieveDestroy.as_view(), name='like_retrieve_delete' ),
    path('api/profile/', views.ProfileListCreate.as_view(), name='profile_list_create' ),
    path('api/profile/<int:user>/', views.ProfileRetrieveUpdate.as_view(), name='profile_retrieve_update' ),
    path('api/token-auth/', obtain_jwt_token),
    path('api/current-user/', current_user),
    path('api/users/', UserList.as_view()),
]
