# Generated by Django 3.0.7 on 2020-06-18 20:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('twitter_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='picture',
            field=models.ImageField(blank=True, help_text='Profile picture', null=True, upload_to=''),
        ),
    ]
