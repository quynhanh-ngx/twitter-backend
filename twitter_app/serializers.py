from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_jwt.settings import api_settings

from .models import Tweet, Like, Profile

User = get_user_model()


class TweetSerializer(serializers.ModelSerializer):
    author_name = serializers.SerializerMethodField()
    author_picture = serializers.SerializerMethodField()

    def get_author_name(self, obj):
        return obj.author.first_name + ' ' + obj.author.last_name


    def get_author_picture(self, obj):
        # TODO : don't use hard coded media host
        return 'http://127.0.0.1:8000' + settings.MEDIA_URL + (str(Profile.objects.get_or_create(user=obj.author)[0].picture) or 'unknown.jpg')

    class Meta:
        model = Tweet
        fields = ('id', 'author', 'message', 'created_at', 'like_count', 'author_name', 'author_picture')


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ('id', 'user', 'tweet')


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('user', 'picture')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username',)


class UserSerializerWithToken(serializers.ModelSerializer):

    token = serializers.SerializerMethodField()
    password = serializers.CharField(write_only=True)

    def get_token(self, obj):
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(obj)
        token = jwt_encode_handler(payload)
        return token

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    class Meta:
        model = User
        fields = ('token', 'username', 'password')
