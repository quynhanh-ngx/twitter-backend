from django.shortcuts import render

# Create your views here.
from .models import Tweet, Like, Profile
from .serializers import TweetSerializer, LikeSerializer, ProfileSerializer
from rest_framework import generics


class TweetListCreate(generics.ListCreateAPIView):
    queryset = Tweet.objects.all()
    serializer_class = TweetSerializer


class TweetRetrieveDestroy(generics.RetrieveDestroyAPIView):
    queryset = Tweet.objects.all()
    serializer_class = TweetSerializer


class LikeListCreate(generics.ListCreateAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer


class LikeRetrieveDestroy(generics.RetrieveDestroyAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer


class ProfileListCreate(generics.ListCreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class ProfileRetrieveUpdate(generics.RetrieveUpdateAPIView):
    lookup_field = 'user'
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
