from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, help_text='User the profile belongs to')
    picture = models.ImageField(help_text='Profile picture')


class Tweet(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, help_text='Author of the tweet')
    message = models.CharField(max_length=280, help_text='Message of the tweet')


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, help_text='User who likes the tweet')
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE, help_text='Tweet the user likes')

    class Meta:
        unique_together = [('user', 'tweet')]
