from django.shortcuts import render

# Create your views here.
from .models import Tweet
from .serializers import TweetSerializer
from rest_framework import generics


class TweetListCreate(generics.ListCreateAPIView):
    queryset = Tweet.objects.all()
    serializer_class = TweetSerializer
