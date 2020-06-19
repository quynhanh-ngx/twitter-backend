from django.shortcuts import render

# Create your views here.
from .models import Tweet, Like
from .serializers import TweetSerializer, LikeSerializer
from rest_framework import generics


class TweetListCreate(generics.ListCreateAPIView):
    queryset = Tweet.objects.all()
    serializer_class = TweetSerializer


class LikeListCreate(generics.ListCreateAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer


class LikeDestroy(generics.DestroyAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
