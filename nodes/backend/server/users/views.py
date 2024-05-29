from django.shortcuts import render
from rest_framework.exceptions import ValidationError
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

# serializers
from .serializers import UserRegisterSerializer
from .serializers import UserLoginSerializer


class UserLoginAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            response = {
                "username": {
                    "detail": "Invalid request body"
                }
            }
            user = authenticate(username=request.data['username'], password=request.data['password'])
            if user is not None:
                token, created = Token.objects.get_or_create(user=user)
                response = {
                    'success': True,
                    'username': user.username,
                    'email': user.email,
                    'token': token.key
                }
                return Response(response, status=status.HTTP_200_OK)
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
    

class UserRegisterAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response = {
                'success': True,
                'user': serializer.data,
                'token': Token.objects.get(user=User.objects.get(username=serializer.data['username'])).key
            }
            return Response(response, status=status.HTTP_200_OK)
        raise ValidationError(
            serializer.errors, code=status.HTTP_400_BAD_REQUEST
        )
    
class UserLogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args):
        token = Token.objects.get(user=request.user)
        token.delete()
        return Response({'success': True, 'detail':'Logget out!' },
                        status=status.HTTP_200_OK)