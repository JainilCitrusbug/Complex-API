# Generated by Django 3.1.4 on 2022-04-18 11:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0002_auto_20220418_1711'),
    ]

    operations = [
        migrations.AddField(
            model_name='song',
            name='song_image',
            field=models.ImageField(blank=True, null=True, upload_to='images/song/'),
        ),
    ]