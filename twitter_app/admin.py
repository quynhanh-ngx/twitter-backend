from django.contrib import admin

# Register your models here.
from twitter_app.models import Profile, Tweet, Like, TweetImage


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    pass


@admin.register(Tweet)
class TweetAdmin(admin.ModelAdmin):
    pass


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    pass


@admin.register(TweetImage)
class TweetImageAdmin(admin.ModelAdmin):
    pass
