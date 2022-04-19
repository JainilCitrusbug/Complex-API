from multiprocessing import AuthenticationError
import random 
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import *
from .serializers import *
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
import jwt, datetime

# Create your views here.

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
        user = CustomUser.objects.filter(mobile=mobile).first()
        print(user)
        if mobile:
            otp = random.randrange(111111, 999999)
            user.otp = otp
            user.save()
            return JsonResponse({'OTP': otp})

#----------------------------------------------------------------------------------------------
# Login API
#----------------------------------------------------------------------------------------------

class LoginView(APIView):
    def get(self, request):
        mobile = request.GET.get('mobile')
        otp = request.GET.get('otp')
        user = CustomUser.objects.filter(mobile=mobile, otp=otp).first()

        if user :
            payload = {
                'id' : user.id,
                'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
                'iat' : datetime.datetime.utcnow()
            }

            token = jwt.encode(payload, 'secret', algorithm='HS256')
            response = Response()
            response.set_cookie(key='jwt', value=token)
            response.data = {'jwt' : token}
            return response
        else:
            return JsonResponse({'error':'USer does not exist !!!'})

#----------------------------------------------------------------------------------------------
# Artist
#----------------------------------------------------------------------------------------------

class ArtistView(APIView):

    def get(self, request, id=None):
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
        serializer = ArtistSerializers(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data,safe=False)
        else:
            return JsonResponse(serializer.errors) 


class ArtistSongListView(APIView):
    def get(self, request):
        artist = Artist.objects.all()
        serializer = ArtistSongListSerializers(artist, many=True)
        return JsonResponse(serializer.data, safe=False)

#----------------------------------------------------------------------------------------------
# Song
#----------------------------------------------------------------------------------------------

class SongView(APIView):
    def get(self, request, id=None):
        if id is not None:
            song = Song.objects.get(id=id)
            serializer = SongSerializers(song)
            return JsonResponse(serializer.data)
        else:
            song = Song.objects.all()
            serializer = SongSerializers(song, many=True)
            return JsonResponse(serializer.data, safe=False)

    @csrf_exempt
    def post(self, request):
        serializer = SongSerializers(data = request.data)
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
        if id is not None:
            playlist = Playlist.objects.get(id=id)
            serializer = PlaylistSerializers(playlist)
            return JsonResponse(serializer.data,safe=False)
        else:
            playlist = Playlist.objects.all()
            serializer = PlaylistListViewSerializers(playlist, many=True)
            return JsonResponse(serializer.data,safe=False) 

    @csrf_exempt
    def post(self, request):
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
        token = request.COOKIES.get('jwt')
        if not token:
            return JsonResponse({'error':'Unauthentication !'})
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except:
            return JsonResponse({'error':'Unauthentication !'})
        user = CustomUser.objects.get(id=payload['id'])
        playlist = Playlist.objects.filter(user__email=user)
        serializer = PlaylistListViewSerializers(playlist, many=True)
        return JsonResponse(serializer.data, safe=False)