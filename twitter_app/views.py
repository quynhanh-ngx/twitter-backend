from functools import reduce

from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Tweet, Like, Profile
from .serializers import TweetSerializer, LikeSerializer, ProfileSerializer, UserSerializer, UserSerializerWithToken
from rest_framework import generics, permissions, status


from django.db.models import Q
import operator


class TweetListCreate(generics.ListCreateAPIView):
    queryset = Tweet.objects.all()
    serializer_class = TweetSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class TweetListByAuthor(generics.ListAPIView):
    serializer_class = TweetSerializer

    def get_queryset(self):
        return Tweet.objects.filter(author=self.kwargs['author'])


class TweetRetrieveDestroy(generics.RetrieveDestroyAPIView):
    queryset = Tweet.objects.all()
    serializer_class = TweetSerializer

    def perform_destroy(self, tweet):
        if tweet.author == self.request.user:
            super().perform_destroy(tweet)
        else:
            raise PermissionDenied()


class LikeListCreate(generics.ListCreateAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class LikeRetrieveDestroy(generics.RetrieveDestroyAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer

    def get_object(self):
        queryset = self.get_queryset()  # Get the base queryset
        queryset = self.filter_queryset(queryset)  # Apply any filter backends
        filter = {
            'user': self.request.user.pk,
            'tweet': self.kwargs['tweet']
        }
        q = reduce(operator.and_, (Q(x) for x in filter.items()))
        return get_object_or_404(queryset, q)

    def perform_destroy(self, like):
        if like.user == self.request.user:
            super().perform_destroy(like)
        else:
            raise PermissionDenied()


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

