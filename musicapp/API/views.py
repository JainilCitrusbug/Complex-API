import random
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import *
from .serializers import *
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
import jwt, datetime

# Create your views here.

def authentication(request):
    try:
        token = request.COOKIES.get('jwt')
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        return payload
    except:
        return None

#----------------------------------------------------------------------------------------------
# Create User
#----------------------------------------------------------------------------------------------

class UserAPI(APIView):
    @csrf_exempt
    def post(self, request):
        serializer = UserSerializers(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data,safe=False)
        else:
            return JsonResponse(serializer.errors) 

#----------------------------------------------------------------------------------------------
# Create OTP
#----------------------------------------------------------------------------------------------

class OTP(APIView):
    def get(self, request):
        mobile = request.GET.get('mobile')
        if mobile:
            user = CustomUser.objects.get(mobile=mobile)
            if mobile:
                otp = random.randrange(111111, 999999)
                user.otp = otp
                user.save()
                return JsonResponse({'OTP': otp})
        else:
            return JsonResponse({'error':'Please enter mobile number !!!'})

#----------------------------------------------------------------------------------------------
# Login API
#----------------------------------------------------------------------------------------------

class LoginView(APIView):
    @csrf_exempt
    def post(self, request):
        mobile = request.POST.get('mobile')
        otp = request.POST.get('otp')
        if mobile and otp:
            user = CustomUser.objects.get(mobile=mobile, otp=otp)
            if user :
                payload = {
                    'id' : user.id,
                    'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
                    'iat' : datetime.datetime.utcnow()
                }
                token = jwt.encode(payload, 'secret', algorithm='HS256')
                response = Response()
                response.set_cookie(key='jwt', value=token, httponly=True)
                response.data = {'jwt' : token}
                return response
            else:
                return JsonResponse({'error':'User does not exist !!!'})
        else:
            return JsonResponse({'error':'Incorrect mobile number and otp !!!'})

#----------------------------------------------------------------------------------------------
# Artist
#----------------------------------------------------------------------------------------------

class ArtistView(APIView):

    def get(self, request, id=None):
        if authentication(request) == None:
            return JsonResponse({'Error':'Unauthenticated !'})
        else:
            if id is not None:
                artist = Artist.objects.get(id=id)
                serializer = ArtistListAndDetailsSerializers(artist)
                return JsonResponse(serializer.data)
            else:
                artist = Artist.objects.all()
                serializer = ArtistListAndDetailsSerializers(artist, many=True)
                return JsonResponse(serializer.data, safe=False)


    @csrf_exempt
    def post(self, request):
        if authentication(request) == None:
            return JsonResponse({'Error':'Unauthenticated !'})
        else:
            serializer = ArtistSerializers(data = request.data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data,safe=False)
            else:
                return JsonResponse(serializer.errors) 


class ArtistSongListView(APIView):
    def get(self, request, id=None):
        if authentication(request) == None:
            return JsonResponse({'Error':'Unauthenticated !'})
        else:
            if id is not None:
                artist = Artist.objects.get(id=id)
                serializer = ArtistSongListSerializers(artist)
                return JsonResponse(serializer.data)
            else:
                artist = Artist.objects.all()
                serializer = ArtistSongListSerializers(artist, many=True)
                return JsonResponse(serializer.data, safe=False)

#----------------------------------------------------------------------------------------------
# Song
#----------------------------------------------------------------------------------------------

class SongView(APIView):
    def get(self, request, id=None):
        if authentication(request) == None:
            return JsonResponse({'Error':'Unauthenticated !'})
        else:
            genre = request.GET.get('genre')
            language = request.GET.get('language')
            artist = request.GET.get('artist')
            songs = request.GET.get('song')
            if id is not None:
                song = Song.objects.get(id=id)
                serializer = SongSerializers(song)
            else:
                song = Song.objects.all()
                if genre:
                    song = song.filter(genre__genre_name__icontains=genre)
                if language:
                    song = song.filter(language__icontains=language)
                if artist:
                    song = song.filter(artist__artist_name__icontains=artist)
                if songs:
                    song = song.filter(song_name__icontains=songs)
                serializer = SongSerializers(song, many=True)
            return JsonResponse(serializer.data, safe=False)

    @csrf_exempt
    def post(self, request):
        if authentication(request) == None:
            return JsonResponse({'Error':'Unauthenticated !'})
        else:
            serializer = AddSongSerializers(data = request.data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data,safe=False)
            else:
                return JsonResponse(serializer.errors)

#----------------------------------------------------------------------------------------------
# Playlist
#----------------------------------------------------------------------------------------------

class PlaylistView(APIView):
    def get(self, request, id = None):
        if authentication(request) == None:
            return JsonResponse({'Error':'Unauthenticated !'})
        else:
            genre = request.GET.get('genre')
            language = request.GET.get('language')
            artist = request.GET.get('artist')
            songs = request.GET.get('song')
            name = request.GET.get('name')
            featured = request.GET.get('featured')
            if id is not None:
                playlist = Playlist.objects.get(id=id)
                serializer = PlaylistSerializers(playlist)
            else:
                playlist = Playlist.objects.all()
                if genre:
                    playlist = playlist.filter(song__genre__genre_name__icontains=genre)
                    serializer = PlaylistSerializers(playlist, many=True)
                elif language:
                    playlist = playlist.filter(song__language__icontains=language)
                    serializer = PlaylistSerializers(playlist, many=True)
                elif artist:
                    playlist = playlist.filter(song__artist__artist_name__icontains=artist)
                    serializer = PlaylistSerializers(playlist, many=True)
                elif songs:
                    playlist = playlist.filter(song__song_name__icontains=songs)
                    serializer = PlaylistSerializers(playlist, many=True)
                elif name:
                    playlist = playlist.filter(playlist_name__icontains=name)
                    serializer = PlaylistSerializers(playlist, many=True)
                elif featured:
                    playlist = playlist.filter(is_featured__icontains=featured)
                    serializer = PlaylistSerializers(playlist, many=True)
                else:
                    serializer = PlaylistListViewSerializers(playlist, many=True)
            return JsonResponse(serializer.data,safe=False) 

    @csrf_exempt
    def post(self, request):
        if authentication(request) == None:
            return JsonResponse({'Error':'Unauthenticated !'})
        else:
            serializer = PlaylistSerializers(data = request.data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data,safe=False)
            else:
                return JsonResponse(serializer.errors)

#----------------------------------------------------------------------------------------------
# User Playlist
#----------------------------------------------------------------------------------------------

class UserPlaylistView(APIView):
    def get(self, request):
        # token = request.COOKIES.get('jwt')
        # if not token:
        #     return JsonResponse({'error':'Unauthenticated !'})
        # try:
        #     payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        # except:
        #     return JsonResponse({'error':'Unauthenticated !'})
        if authentication(request) == None:
            return JsonResponse({'Error':'Unauthenticated !'})
        else:
            user = CustomUser.objects.get(id=authentication(request)['id'])
            playlist = Playlist.objects.filter(user__email=user)
            serializer = PlaylistListViewSerializers(playlist, many=True)
            return JsonResponse(serializer.data, safe=False)



