import random 
from django.http import JsonResponse
from requests import Response
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
    @csrf_exempt
    def post(self, request):
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
            return JsonResponse({'token' : token})

#----------------------------------------------------------------------------------------------
# Add Artist
#----------------------------------------------------------------------------------------------

class ArtistView(APIView):
    @csrf_exempt
    def post(self, request):
        serializer = ArtistSerializers(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data,safe=False)
        else:
            return JsonResponse(serializer.errors) 

#----------------------------------------------------------------------------------------------
# Add Song
#----------------------------------------------------------------------------------------------

class SongView(APIView):
    def get(self, request):
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