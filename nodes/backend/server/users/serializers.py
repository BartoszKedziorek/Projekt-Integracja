from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError
from rest_framework import status
from rest_framework.authtoken.models import Token
from drf_spectacular.utils import extend_schema_serializer, OpenApiExample
from django.contrib.auth.models import Group


class UserLoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password']


class UserRegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'first_name',
                  'last_name', 'email', 'password',
                  'password2']
    
    def validate_username(sefl, username):
        if User.objects.filter(username=username).exists():
            detail = {
                "detail": "User Already exists!"
            }
            raise ValidationError(detail=detail)
        return username 

    def validate(self, instance):
        if instance['password'] != instance['password2']:
            raise ValidationError({"message":"Both password must match"})
        
        if User.objects.filter(email=instance['email']).exists():
            raise ValidationError({"message": "Email already taken!"})

        return instance
    
    def create(self, validated_data):
        # metoda tworząca użytkownika oraz token
        password = validated_data.pop('password')
        password2 = validated_data.pop('password2')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        Token.objects.create(user=user)
        return user


class RoleSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    
    class Meta:
        model = Group
        fields = ['name']
    

    
