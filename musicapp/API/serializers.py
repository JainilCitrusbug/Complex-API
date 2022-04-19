from .models import *
from rest_framework import serializers

class UserSerializers(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ['id','username','email','mobile','otp']

    def create(self, validated_data):
        return super().create(validated_data)

class ArtistSerializers(serializers.ModelSerializer):

    class Meta:
        model = Artist
        fields = '__all__'

    def create(self, validated_data):
        return super().create(validated_data)

class GenreSerializers(serializers.ModelSerializer):
    
    class Meta:
        model = Genre
        fields = '__all__'

class SongSerializers(serializers.ModelSerializer):

    artist = ArtistSerializers(many = True)
    
    class Meta:
        model = Song
        fields = ['id','song_name','audio_file','song_image','artist','language','genre']

    def create(self, validated_data):
        return super().create(validated_data)

class ArtistListAndDetailsSerializers(serializers.ModelSerializer):

    Song_Count = serializers.SerializerMethodField('get_song_count')

    def get_song_count(self, artist):
        return Song.objects.filter(artist__artist_name = artist).count()

    class Meta:
        model = Artist
        fields = ['id','artist_name','artist_image','Song_Count']

class PlaylistSerializers(serializers.ModelSerializer):
    
    Song_Count = serializers.SerializerMethodField('get_song_count')

    def get_song_count(self, playlist):
        return playlist.song.all().count()

    song = SongSerializers(many = True)

    class Meta:
        model = Playlist
        fields = ['id','playlist_name','Song_Count','playlist_image','song','is_featured']

    def create(self, validated_data):
        return super().create(validated_data)

class PlaylistListViewSerializers(serializers.ModelSerializer):

    Song_Count = serializers.SerializerMethodField('get_song_count')

    def get_song_count(self, playlist):
        return playlist.song.all().count()

    class Meta:
        model = Playlist
        fields = ['id','playlist_name','Song_Count','playlist_image','is_featured']

class ArtistSongSerializers(serializers.ModelSerializer):
    
    class Meta:
        model = Song
        fields = ['id','song_name','audio_file','song_image','language','genre']

class ArtistSongListSerializers(serializers.ModelSerializer):

    Song_Count = serializers.SerializerMethodField('get_song_count')
    songs = serializers.SerializerMethodField('get_song')

    def get_song_count(self, artist):
        return Song.objects.filter(artist__artist_name = artist).count()

    def get_song(self, artist):
        serializer = ArtistSongSerializers(Song.objects.filter(artist__artist_name = artist),many=True)
        
        return serializer.data


    class Meta:
        model = Artist
        fields = ['id','artist_name','artist_image','Song_Count','songs']