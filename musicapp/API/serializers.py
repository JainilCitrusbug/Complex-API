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
    
    class Meta:
        model = Song
        fields = ['song_name','audio_file','song_image','artist','language','genre']

    def create(self, validated_data):
        return super().create(validated_data)