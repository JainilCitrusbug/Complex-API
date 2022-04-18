from pyexpat import model
from django.db import models
# from django.contrib.auth.models import AbstractUser, AbstractBaseUser
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.models import BaseUserManager

# Create your models here.

class AccountManager(BaseUserManager):
    def create_user(self, email, password=None, **kwargs):
        if not email:
            raise ValueError("Users must have a valid email address.")

        if not kwargs.get("username"):
            raise ValueError("Users must have a valid username.")

        account = self.model(
            email=self.normalize_email(email), username=kwargs.get("username")
        )

        account.set_password(password)
        account.save()

        return account

    def create_superuser(self, email, password, **kwargs):
        account = self.create_user(email, password, **kwargs)

        account.is_superuser = True
        account.is_staff = True
        account.save()

        return account

class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(unique=True, max_length=50)
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    mobile = models.IntegerField(unique=True, blank=True, null=True)
    otp = models.IntegerField(blank=True, null=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = AccountManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

class Artist(models.Model):
    artist_name = models.CharField(max_length=50)
    artist_image = models.ImageField(upload_to="images/artist/", blank=True, null=True)

class Genre(models.Model):
    genre_name = models.CharField(max_length=50)
    genre_image = models.ImageField(upload_to="images/genre/", blank=True, null=True)

class Song(models.Model):
    song_name = models.CharField(max_length=100)
    audio_file = models.FileField(upload_to="audio/", blank=True, null=True)
    song_image = models.ImageField(upload_to="images/song/", blank=True, null=True)
    artist = models.ManyToManyField(Artist)
    language = models.CharField(max_length=20)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)

class Playlist(models.Model):
    playlist_name = models.CharField(max_length=50)
    song = models.ManyToManyField(Song)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    is_featured = models.BooleanField(default=False)
    playlist_image = models.ImageField(upload_to="images/playlist/", blank=True, null=True)

