# Generated by Django 3.0.7 on 2020-07-02 19:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('twitter_app', '0007_tweet_is_retweet'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tweet',
            name='message',
            field=models.CharField(blank=True, default='', help_text='Message of the tweet', max_length=280),
        ),
    ]
