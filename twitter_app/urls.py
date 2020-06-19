from django.urls import path
from . import views

urlpatterns = [
    path('api/tweet/', views.TweetListCreate.as_view() ),
]
