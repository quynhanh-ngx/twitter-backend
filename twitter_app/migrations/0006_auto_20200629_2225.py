# Generated by Django 3.0.7 on 2020-06-29 22:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('twitter_app', '0005_auto_20200624_1722'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tweet',
            name='message',
            field=models.CharField(blank=True, help_text='Message of the tweet', max_length=280, null=True),
        ),
    ]
