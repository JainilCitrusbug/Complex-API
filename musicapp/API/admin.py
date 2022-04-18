from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(CustomUser)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username','email','name','gender','mobile','otp']

@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    list_display = ['id','artist_name','artist_image']

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ['id','genre_name','genre_image']

admin.site.register(Song)
# class SongAdmin(admin.ModelAdmin):
#     list_display = ['id', 'song_name','audio_file','artist','language','genre']

admin.site.register(Playlist)
# class PlaylistAdmin(admin.ModelAdmin):
#     list_display = ['id', 'playlist_name','song','user','is_featured','playlist_image']