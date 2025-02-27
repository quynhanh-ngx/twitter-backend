from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_jwt.settings import api_settings

from .models import Tweet, Like, Profile, TweetImage

User = get_user_model()


class TweetImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = TweetImage
        fields = ('image',)
        read_only_fields = ("tweet",)


class TweetSerializer(serializers.ModelSerializer):
    author_name = serializers.SerializerMethodField()
    author_picture = serializers.SerializerMethodField()
    author = serializers.ReadOnlyField(source='author.username')
    liked = serializers.SerializerMethodField()
    retweet_id = serializers.SerializerMethodField()
    images = TweetImageSerializer(many=True, required=False)

    def get_liked(self, obj):
        """
        :return: whether the current user has liked this tweet
        """
        user = self._get_user_if_exists()
        return Like.objects.filter(user=user, tweet_id=obj.id).exists()

    def get_retweet_id(self, obj):
        """
        :return: whether the current user has retweeted this tweet
        """
        user = self._get_user_if_exists()
        try:
            return Tweet.objects.get(replying_to_id=obj.id,
                                            author=user,
                                            message="",
                                            video="",
                                            images__isnull=True
                                            ).id
        except Tweet.DoesNotExist:
            return None

    def get_author_name(self, obj):
        return obj.author.first_name + ' ' + obj.author.last_name

    def get_author_picture(self, obj):
        # TODO : don't use hard coded media host
        return 'http://127.0.0.1:8000' + settings.MEDIA_URL + (
                str(Profile.objects.get_or_create(user=obj.author)[0].picture) or 'unknown.jpg')

    def validate(self, attrs):
        user = self._get_user_if_exists()
        has_content = any((attrs.get('message'), self.context['view'].request.FILES))
        is_retweet = attrs.get('is_retweet')
        replying_to = attrs.get('replying_to')
        if is_retweet:
            if not replying_to:
                raise serializers.ValidationError(
                    {'is_retweet': 'is_retweet must be False if replying_to is null'}
                )
            # Cannot retweet a blank retweet
            if not replying_to.has_content:
                raise serializers.ValidationError(
                    {'is_retweet': 'Cannot retweet a retweet that doesn\'t have a comment'}
                )
            # Retweet without comment
            if not has_content:
                # Verify user has not already retweeted what they're replying to
                if Tweet.objects.filter(replying_to_id=replying_to,
                                        author=user,
                                        message="",
                                        video="",
                                        images__isnull=True
                                        ).exists():
                    raise serializers.ValidationError(
                        {'is_retweet': 'Cannot retweet something without a comment twice'}
                    )

        elif not has_content:
            raise serializers.ValidationError(
                {'message': 'Tweet cannot be blank if you don\'t provide a video or images unless it\'s a retweet'}
            )
        return attrs

    def _get_user_if_exists(self):
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user
        return user

    def create(self, validated_data):
        images_data = self.context['view'].request.FILES
        tweet = super().create(validated_data)
        image_count = 0
        print("Checking images")
        for key, image_data in images_data.items():
            print(f"Found file {key}={image_data}")
            if key == 'video':
                continue
            # maximum image for a tweet
            if image_count == settings.TWITTER_IMAGES_PER_TWEET:
                break
            TweetImage.objects.create(tweet=tweet, image=image_data)
            image_count += 1
        return tweet

    class Meta:
        model = Tweet
        fields = ('id', 'author', 'message',
                  'created_at', 'like_count', 'author_name',
                  'author_picture', 'liked', 'video', 'images', 'replying_to',
                  'is_retweet', 'retweet_id')


class LikeSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

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
