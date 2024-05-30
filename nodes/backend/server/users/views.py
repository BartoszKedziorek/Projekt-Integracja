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
from drf_spectacular.utils import extend_schema, OpenApiParameter, inline_serializer

# serializers
from .serializers import UserRegisterSerializer
from .serializers import UserLoginSerializer
from rest_framework import serializers
from rest_framework.authentication import TokenAuthentication


class UserLoginAPIView(APIView):
    serializer_class = UserLoginSerializer

    @extend_schema(
            request=serializer_class,
            responses={
                200: inline_serializer(
                    name="LoginSuccessResponse",
                    fields={
                        'username': serializers.CharField(),
                        'token': serializers.CharField()
                    }
                )            
            }
    )
    def post(self, request, *args, **kwargs):
        serializer = UserLoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        user = authenticate(username=request.data['username'], password=request.data['password'])
        if user is None:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        token, created = Token.objects.get_or_create(user=user)
        resp_data = {'token':token.key,
                     'emial': user.email}
        resp_data.update(serializer.data)
        return Response(resp_data, status=status.HTTP_200_OK)
            
        
    
class UserRegisterAPIView(APIView):
    serializer_class = UserRegisterSerializer

    @extend_schema(request=UserRegisterSerializer,
                   responses={
                       200: inline_serializer(name='RegisterSuccessResponse',
                                              fields={
                                                  'success': serializers.BooleanField(),
                                                  'user': UserRegisterSerializer(),
                                                  'token': serializers.CharField()
                                              })
                   })
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
    serializer_class = None
    permission_classes = [IsAuthenticated]

    @extend_schema(responses={
        200:inline_serializer(name='LogoutSuccessResponse',
                              fields={
                                  'success': serializers.BooleanField(),
                                  'detail': serializers.CharField()
                              })
    })
    def post(self, request, *args):
        token = Token.objects.get(user=request.user)
        token.delete()
        return Response({'success': True, 'detail':'Logget out!' },
                        status=status.HTTP_200_OK)