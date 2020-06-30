from typing import Union, List

from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import QuerySet

User = get_user_model()


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, help_text='User the profile belongs to')
    picture = models.ImageField(blank=True, null=True, help_text='Profile picture')

    def __str__(self):
        return f"Profile(user={self.user})"


class Tweet(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, help_text='Author of the tweet')
    message = models.CharField(blank=True, null=True, max_length=280, help_text='Message of the tweet')
    created_at = models.DateTimeField(auto_now_add=True)
    video = models.FileField(blank=True, null=True, upload_to='tweet_media/videos/', help_text='Video for the tweet')
    replying_to = models.ForeignKey('Tweet', blank=True, null=True, on_delete=models.SET_NULL,
                                    help_text="This tweet is replying to")

    def __str__(self):
        return f"Tweet(id={self.id}, author={self.author}, created_at={self.created_at})"

    def get_likes(self) -> Union[QuerySet, List['Like']]:
        return Like.objects.filter(tweet_id=self.id)

    @property
    def like_count(self) -> int:
        return self.get_likes().count()

    class Meta:
        ordering = ['-created_at']


class TweetImage(models.Model):
    tweet = models.ForeignKey('Tweet', related_name='images', on_delete=models.CASCADE,
                              help_text="Tweet the image belongs to")
    image = models.ImageField(upload_to='tweet_media/images/', help_text="Image for a tweet")

    def __str__(self):
        return f"TweetImage(tweet={self.tweet})"


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, help_text='User who likes the tweet')
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE, help_text='Tweet the user likes')

    def __str__(self):
        return f"Like(user={self.user}, tweet={self.tweet})"

    class Meta:
        unique_together = [('user', 'tweet')]
