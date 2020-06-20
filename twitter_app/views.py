from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Tweet, Like, Profile
from .serializers import TweetSerializer, LikeSerializer, ProfileSerializer, UserSerializer, UserSerializerWithToken
from rest_framework import generics, permissions, status


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


@api_view(['GET'])
def current_user(request):
    """
    Determine the current user by their token, and return their data
    """

    serializer = UserSerializer(request.user)
    return Response(serializer.data)


class UserList(APIView):
    """
    Create a new user. It's called 'UserList' because normally we'd have a get
    method here too, for retrieving a list of all User objects.
    """

    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = UserSerializerWithToken(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

